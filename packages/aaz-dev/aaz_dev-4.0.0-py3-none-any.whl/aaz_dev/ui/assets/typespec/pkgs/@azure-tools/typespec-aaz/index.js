import { isGlobalNamespace, isService, getProjectedName, createTypeSpecLibrary, TwoLevelMap, getDoc, isNeverType, isVoidType, isArrayModelType, getDiscriminator, isRecordModelType, getEncode, isNullType, isTemplateDeclaration, getProperty, getFormat, getPattern, getMaxLength, getMinLength, getMaxValue, getMinValue, getMinValueExclusive, getMaxValueExclusive, getMaxItems, getMinItems, resolveEncodedName, emitFile, resolvePath, listServices, projectProgram, ignoreDiagnostics } from '@typespec/compiler';
import { buildVersionProjections } from '@typespec/versioning';
import { isSharedRoute, createMetadataInfo, Visibility, resolveRequestVisibility, getServers, isContentTypeHeader, getQueryParamOptions, getHeaderFieldOptions, getVisibilitySuffix, getStatusCodeDescription, getAllHttpServices, reportIfNoRoutes } from '@typespec/http';
import { getOperationId, isReadonlyProperty, getExtensions, getOpenAPITypeName } from '@typespec/openapi';
import { getClientNameOverride, shouldFlattenProperty, createSdkContext } from '@azure-tools/typespec-client-generator-core';
import { isAzureResource } from '@azure-tools/typespec-azure-resource-manager';
import { getLroMetadata, getUnionAsEnum, getArmResourceIdentifierConfig, getPagedResult } from '@azure-tools/typespec-azure-core';
import { getMultipleOf, getMaxProperties, getMinProperties, getUniqueItems } from '@typespec/json-schema';

// Regexps involved with splitting words in various case formats.
const SPLIT_LOWER_UPPER_RE = /([\p{Ll}\d])(\p{Lu})/gu;
const SPLIT_UPPER_UPPER_RE = /(\p{Lu})([\p{Lu}][\p{Ll}])/gu;
// Used to iterate over the initial split result and separate numbers.
const SPLIT_SEPARATE_NUMBER_RE = /(\d)\p{Ll}|(\p{L})\d/u;
// Regexp involved with stripping non-word characters from the result.
const DEFAULT_STRIP_REGEXP = /[^\p{L}\d]+/giu;
// The replacement value for splits.
const SPLIT_REPLACE_VALUE = "$1\0$2";
// The default characters to keep after transforming case.
const DEFAULT_PREFIX_SUFFIX_CHARACTERS = "";
/**
 * Split any cased input strings into an array of words.
 */
function split(value) {
    let result = value.trim();
    result = result
        .replace(SPLIT_LOWER_UPPER_RE, SPLIT_REPLACE_VALUE)
        .replace(SPLIT_UPPER_UPPER_RE, SPLIT_REPLACE_VALUE);
    result = result.replace(DEFAULT_STRIP_REGEXP, "\0");
    let start = 0;
    let end = result.length;
    // Trim the delimiter from around the output string.
    while (result.charAt(start) === "\0")
        start++;
    if (start === end)
        return [];
    while (result.charAt(end - 1) === "\0")
        end--;
    return result.slice(start, end).split(/\0/g);
}
/**
 * Split the input string into an array of words, separating numbers.
 */
function splitSeparateNumbers(value) {
    const words = split(value);
    for (let i = 0; i < words.length; i++) {
        const word = words[i];
        const match = SPLIT_SEPARATE_NUMBER_RE.exec(word);
        if (match) {
            const offset = match.index + (match[1] ?? match[2]).length;
            words.splice(i, 1, word.slice(0, offset), word.slice(offset));
        }
    }
    return words;
}
/**
 * Convert a string to pascal case (`FooBar`).
 */
function pascalCase(input, options) {
    const [prefix, words, suffix] = splitPrefixSuffix(input, options);
    const lower = lowerFactory(options?.locale);
    const upper = upperFactory(options?.locale);
    const transform = pascalCaseTransformFactory(lower, upper);
    return prefix + words.map(transform).join("") + suffix;
}
function lowerFactory(locale) {
    return (input) => input.toLocaleLowerCase(locale);
}
function upperFactory(locale) {
    return (input) => input.toLocaleUpperCase(locale);
}
function pascalCaseTransformFactory(lower, upper) {
    return (word, index) => {
        const char0 = word[0];
        const initial = index > 0 && char0 >= "0" && char0 <= "9" ? "_" + char0 : upper(char0);
        return initial + lower(word.slice(1));
    };
}
function splitPrefixSuffix(input, options = {}) {
    const splitFn = options.split ?? (options.separateNumbers ? splitSeparateNumbers : split);
    const prefixCharacters = options.prefixCharacters ?? DEFAULT_PREFIX_SUFFIX_CHARACTERS;
    const suffixCharacters = options.suffixCharacters ?? DEFAULT_PREFIX_SUFFIX_CHARACTERS;
    let prefixIndex = 0;
    let suffixIndex = input.length;
    while (prefixIndex < input.length) {
        const char = input.charAt(prefixIndex);
        if (!prefixCharacters.includes(char))
            break;
        prefixIndex++;
    }
    while (suffixIndex > prefixIndex) {
        const index = suffixIndex - 1;
        const char = input.charAt(index);
        if (!suffixCharacters.includes(char))
            break;
        suffixIndex = index;
    }
    return [
        input.slice(0, prefixIndex),
        splitFn(input.slice(prefixIndex, suffixIndex)),
        input.slice(suffixIndex),
    ];
}

function getPathWithoutQuery$1(path) {
    // strip everything from the key including and after the ?
    return path.replace(/\/?\?.*/, "");
}
const URL_PARAMETER_PLACEHOLDER = "{}";
// export function swaggerResourcePathToResourceIdTemplate(path: string): string {
//     const pathParts = path.split("?", 2);
//     const urlParts = pathParts[0].split("/");
//     let idx = 1;
//     while (idx < urlParts.length) {
//         if (idx === 1 && /^\{[^{}]*\}$/.test(urlParts[idx])) {
//             // ignore to the parameter name in first part of url, such as `/{parameter}` or `/{parameter}/...`
//             // But the placeholder in first part like `/indexes('{indexname}')` will be processed
//             idx++;
//             continue;
//         }
//         urlParts[idx] = urlParts[idx].replace(/\{[^{}]*\}/g, URL_PARAMETER_PLACEHOLDER);
//         idx++;
//     }
//     pathParts[0] = urlParts.join("/");
//     return pathParts.join("?");
// }
function swaggerResourcePathToResourceId(path) {
    const pathParts = path.split("?", 2);
    const urlParts = pathParts[0].split("/");
    let idx = 1;
    while (idx < urlParts.length) {
        if (idx === 1 && /^\{[^{}]*\}$/.test(urlParts[idx])) {
            idx++;
            continue;
        }
        urlParts[idx] = urlParts[idx].replace(/\{[^{}]*\}/g, URL_PARAMETER_PLACEHOLDER);
        idx++;
    }
    pathParts[0] = urlParts.join("/").toLowerCase();
    return pathParts.join("?");
}
function getResourcePath(program, operation) {
    const { operation: op } = operation;
    let { path: fullPath } = operation;
    if (!isSharedRoute(program, op)) {
        fullPath = getPathWithoutQuery$1(fullPath);
    }
    return fullPath;
}
function getAutorestClientName(context, type) {
    const viaProjection = getProjectedName(context.program, type, "client");
    const clientName = getClientNameOverride(context.sdkContext, type);
    return clientName ?? viaProjection ?? type.name;
}
/**
 * Resolve the OpenAPI operation ID for the given operation using the following logic:
 * - If @operationId was specified use that value
 * - If operation is defined at the root or under the service namespace return `<operation.name>`
 * - Otherwise(operation is under another namespace or interface) return `<namespace/interface.name>_<operation.name>`
 *
 * @param program TypeSpec Program
 * @param operation Operation
 * @returns Operation ID in this format `<name>` or `<group>_<name>`
 */
function resolveOperationId(context, operation) {
    const { operation: op } = operation;
    const explicitOperationId = getOperationId(context.program, op);
    if (explicitOperationId) {
        return explicitOperationId;
    }
    const operationName = getAutorestClientName(context, op);
    if (op.interface) {
        return pascalCaseForOperationId(`${getAutorestClientName(context, op.interface)}_${operationName}`);
    }
    const namespace = op.namespace;
    if (namespace === undefined ||
        isGlobalNamespace(context.program, namespace) ||
        isService(context.program, namespace)) {
        return pascalCase(operationName);
    }
    return pascalCaseForOperationId(`${namespace.name}_${operationName}`);
}
// export function getResourceID(program: Program, operation: HttpOperation): string {
//     const { operation: op } = operation;
//     let { path: fullPath } = operation;
//     if (!isSharedRoute(program, op)) {
//         fullPath = getPathWithoutQuery(fullPath);
//     }
//     return swaggerResourcePathToResourceId(fullPath);
// }
function pascalCaseForOperationId(name) {
    return name
        .split("_")
        .map((s) => pascalCase(s))
        .join("_");
}

const EmitterOptionsSchema = {
    type: "object",
    additionalProperties: true,
    properties: {
        operation: {
            type: "string",
            enum: ["list-resources", "get-resources-operations"],
        },
        "api-version": {
            type: "string",
            nullable: true,
        },
        resources: {
            type: "array",
            items: {
                type: "string",
            },
            nullable: true,
        },
    },
    required: ["operation"],
};
const libDef = {
    name: "@azure-tools/typespec-aaz",
    diagnostics: {
        "Duplicated-success-202": {
            severity: "error",
            messages: {
                default: "Duplicated 202 responses",
            }
        },
        "Duplicated-success-204": {
            severity: "error",
            messages: {
                default: "Duplicated 202 responses",
            }
        },
        "Duplicated-redirect": {
            severity: "error",
            messages: {
                default: "Duplicated redirect responses",
            }
        },
        "missing-status-codes": {
            severity: "error",
            messages: {
                default: "Missing status codes",
            }
        },
        "duplicate-body-types": {
            severity: "error",
            messages: {
                default: "Duplicate body types",
            }
        },
        "Unsupported-Type": {
            severity: "error",
            messages: {
                default: "Unsupported type",
            }
        },
        "union-null": {
            severity: "error",
            messages: {
                default: "Union with null",
            }
        },
        "union-unsupported": {
            severity: "error",
            messages: {
                default: "Union with unsupported type",
            }
        },
        "unsupported-status-code-range": {
            severity: "error",
            messages: {
                default: "Unsupported status code range",
            }
        },
        "invalid-default": {
            severity: "error",
            messages: {
                default: "Invalid default value",
            }
        },
        "missing-host-parameter": {
            severity: "error",
            messages: {
                default: "Missing host parameter",
            }
        }
    },
    emitter: {
        options: EmitterOptionsSchema,
    }
};
const $lib = createTypeSpecLibrary(libDef);
const { reportDiagnostic, createStateSymbol, getTracer } = $lib;

class Ref {
    value;
    toJSON() {
        return this.value;
    }
}
class ClsType {
    pendingSchema;
    constructor(pendingSchema) {
        this.pendingSchema = pendingSchema;
    }
    toJSON() {
        return "@" + this.pendingSchema.ref.toJSON();
    }
}
class ArrayType {
    itemType;
    constructor(itemType) {
        this.itemType = itemType;
    }
    toJSON() {
        return `array<${JSON.parse(JSON.stringify(this.itemType))}>`;
    }
}

function retrieveAAZOperation(context, operation, pathItem) {
    context.tracer.trace("RetrieveOperation", `${operation.verb} ${operation.path}`);
    if (!pathItem) {
        pathItem = {};
    }
    const verb = operation.verb;
    const opId = resolveOperationId(context, operation);
    if (!pathItem[verb]) {
        pathItem[verb] = {};
    }
    pathItem[verb].operationId = opId;
    pathItem[verb].pageable = extractPagedMetadata(context.program, operation);
    const metadateInfo = createMetadataInfo(context.program, {
        canonicalVisibility: Visibility.Read,
    });
    const typeNameOptions = {
        // shorten type names by removing TypeSpec and service namespace
        namespaceFilter(ns) {
            return !isService(context.program, ns);
        },
    };
    const opContext = {
        ...context,
        typeNameOptions,
        metadateInfo,
        operationId: opId,
        visibility: Visibility.Read,
        pendingSchemas: new TwoLevelMap(),
        refs: new TwoLevelMap(),
    };
    const verbVisibility = resolveRequestVisibility(context.program, operation.operation, verb);
    if (verb === 'get') {
        opContext.visibility = Visibility.Query;
        pathItem[verb].read = convert2CMDOperation(opContext, operation);
        processPendingSchemas(opContext, verbVisibility, "read");
    }
    else if (verb === 'head') {
        opContext.visibility = Visibility.Query;
        pathItem[verb].read = convert2CMDOperation(opContext, operation);
        processPendingSchemas(opContext, verbVisibility, "read");
    }
    else if (verb === 'delete') {
        opContext.visibility = Visibility.Delete;
        pathItem[verb].create = convert2CMDOperation(opContext, operation);
        processPendingSchemas(opContext, verbVisibility, "create");
    }
    else if (verb === 'post') {
        opContext.visibility = Visibility.Create;
        pathItem[verb].create = convert2CMDOperation(opContext, operation);
        processPendingSchemas(opContext, verbVisibility, "create");
    }
    else if (verb === 'put') {
        opContext.visibility = Visibility.Create;
        pathItem[verb].create = convert2CMDOperation(opContext, operation);
        processPendingSchemas(opContext, verbVisibility, "create");
        opContext.visibility = Visibility.Update;
        opContext.pendingSchemas.clear();
        opContext.refs.clear();
        pathItem[verb].update = convert2CMDOperation(opContext, operation);
        processPendingSchemas(opContext, verbVisibility, "update");
    }
    else if (verb === 'patch') {
        opContext.visibility = Visibility.Update;
        pathItem[verb].update = convert2CMDOperation(opContext, operation);
        processPendingSchemas(opContext, verbVisibility, "update");
    }
    else {
        console.log(" verb not expected: ", verb);
    }
    return pathItem;
}
function convert2CMDOperation(context, operation) {
    // TODO: resolve host parameters for the operation
    const hostPathAndParameters = extractHostPathAndParameters(context);
    const hostPath = hostPathAndParameters?.hostPath ?? "";
    const op = {
        operationId: context.operationId,
        description: getDoc(context.program, operation.operation),
        http: {
            // merge host path and operation path
            path: hostPath + getPathWithoutQuery(operation.path),
        }
    };
    let lroMetadata = getLroMetadata(context.program, operation.operation);
    if (operation.verb === "get") {
        lroMetadata = undefined;
    }
    if (lroMetadata !== undefined && operation.verb !== "get") {
        op.longRunning = {
            finalStateVia: lroMetadata.finalStateVia,
        };
        // TODO: add support for custom polling information
    }
    op.http.request = extractHttpRequest(context, operation, hostPathAndParameters?.hostParameters ?? {});
    op.http.responses = extractHttpResponses({
        ...context,
        visibility: Visibility.Read,
    }, operation, lroMetadata);
    return op;
}
function extractHostPathAndParameters(context) {
    const servers = getServers(context.program, context.service.type);
    if (servers === undefined || servers.length > 1) {
        return undefined;
    }
    const server = servers[0];
    // using r"^(.*://)?[^/]*(/.*)$" to split server url into host and path if url matches the pattern else the path should be empty
    const hostPath = server.url.match(/^(.*:\/\/[^/]+)?(\/.*)$/)?.[2] ?? "";
    if (hostPath === "/" || hostPath === "") {
        return undefined;
    }
    // using r"\{([^{}]*)}" to iterate over all parameter names in hostPath, the name should not contain '{' or '}'
    const hostParameters = {};
    const hostPathParameters = hostPath.matchAll(/\{([^{}]*)\}/g);
    for (const match of hostPathParameters) {
        const name = match[1];
        const param = server.parameters?.get(name);
        let schema;
        if (param === undefined) {
            reportDiagnostic(context.program, {
                code: "missing-host-parameter",
                target: context.service.type,
                message: `Host parameter '${name}' is not defined in the server parameters.`,
            });
        }
        else {
            schema = convert2CMDSchema({
                ...context,
                visibility: Visibility.Read,
                supportClsSchema: false,
            }, param, name);
        }
        if (schema === undefined) {
            schema = {
                name,
                type: "string",
            };
        }
        schema.required = true;
        hostParameters[name] = schema;
    }
    return {
        hostPath,
        hostParameters,
    };
}
function extractHttpRequest(context, operation, hostParameters) {
    const request = {
        method: operation.verb,
    };
    let schemaContext;
    const methodParams = operation.parameters;
    const paramModels = {};
    // add host parameters from the host path to path parameters
    if (hostParameters && Object.keys(hostParameters).length > 0) {
        paramModels["path"] = {
            ...hostParameters,
        };
    }
    let clientRequestIdName;
    for (const httpOpParam of methodParams.parameters) {
        if (httpOpParam.type === "header" && isContentTypeHeader(context.program, httpOpParam.param)) {
            continue;
        }
        if (isNeverType(httpOpParam.param.type)) {
            continue;
        }
        schemaContext = buildSchemaEmitterContext(context, httpOpParam.param, httpOpParam.type);
        const schema = convert2CMDSchema(schemaContext, httpOpParam.param, httpOpParam.name);
        if (!schema) {
            continue;
        }
        schema.required = !httpOpParam.param.optional;
        if (paramModels[httpOpParam.type] === undefined) {
            paramModels[httpOpParam.type] = {};
        }
        paramModels[httpOpParam.type][schema.name] = schema;
        if (httpOpParam.type === "header" && schema.name === "x-ms-client-request-id") {
            clientRequestIdName = schema.name;
        }
    }
    if (paramModels["path"]) {
        request.path = {
            params: [],
        };
        // sort by param name
        for (const name of Object.keys(paramModels["path"]).sort()) {
            request.path.params.push(paramModels["path"][name]);
        }
    }
    if (paramModels["query"]) {
        request.query = {
            params: [],
        };
        // sort by param name
        for (const name of Object.keys(paramModels["query"]).sort()) {
            request.query.params.push(paramModels["query"][name]);
        }
    }
    if (paramModels["header"]) {
        request.header = {
            params: [],
        };
        // sort by param name
        for (const name of Object.keys(paramModels["header"]).sort()) {
            request.header.params.push(paramModels["header"][name]);
        }
        if (clientRequestIdName) {
            request.header.clientRequestId = clientRequestIdName;
        }
    }
    if (methodParams.body && !isVoidType(methodParams.body.type)) {
        const body = methodParams.body;
        const consumes = body.contentTypes ?? [];
        if (consumes.length === 0) {
            // we didn't find an explicit content type anywhere, so infer from body.
            if (getModelOrScalarTypeIfNullable(body.type)) {
                consumes.push("application/json");
            }
        }
        if (body.bodyKind === "multipart") {
            throw new Error("NotImplementedError: Multipart form data payloads are not supported.");
        }
        if (isBinaryPayload(body.type, consumes)) {
            throw new Error("NotImplementedError: Binary payloads are not supported.");
        }
        if (consumes.includes("multipart/form-data")) {
            throw new Error("NotImplementedError: Multipart form data payloads are not supported.");
        }
        let schema;
        if (body.property) {
            context.tracer.trace("RetrieveBody", context.visibility.toString());
            schemaContext = buildSchemaEmitterContext(context, body.property, "body");
            schema = convert2CMDSchema(schemaContext, body.property, getJsonName(context, body.property));
            schema.required = !body.property.optional;
        }
        else {
            schemaContext = buildSchemaEmitterContext(context, body.type, "body");
            schema = {
                ...convert2CMDSchemaBase(schemaContext, body.type),
                name: "body",
                required: true,
            };
        }
        if (schema !== undefined) {
            // schema.required = !methodParams.body.type.optional;
            if (schema.type === "object") {
                schema = {
                    ...schema,
                    clientFlatten: true,
                };
            }
            request.body = {
                json: {
                    schema
                }
            };
        }
    }
    return request;
}
function extractHttpResponses(context, operation, lroMetadata) {
    let success202Response; // only one success 202 response is allowed
    let success204Response; // only one success 204 response is allowed
    let success2xxResponse; // only one success 2xx(except 202 and 204) response is allowed
    let redirectResponse;
    const errorResponses = [];
    for (const response of operation.responses) {
        let statusCodes = getOpenAPI2StatusCodes(context, response.statusCodes, response.type);
        if (statusCodes.length === 0) {
            reportDiagnostic(context.program, {
                code: "missing-status-codes",
                target: response.type,
            });
        }
        if (statusCodes.includes("default")) {
            errorResponses.push(convert2CMDHttpResponse(context, response, undefined, true));
            continue;
        }
        const isSuccess = statusCodes.map((code) => code.startsWith("2")).includes(true);
        const isRedirect = statusCodes.map((code) => code.startsWith("3")).includes(true);
        const isError = !isSuccess && !isRedirect;
        if (isSuccess) {
            if (statusCodes.includes("202")) {
                if (success202Response !== undefined) {
                    reportDiagnostic(context.program, {
                        code: "Duplicated-success-202",
                        target: response.type,
                    });
                }
                success202Response = convert2CMDHttpResponse(context, response, ["202"], false);
            }
            if (statusCodes.includes("204")) {
                if (success204Response !== undefined) {
                    reportDiagnostic(context.program, {
                        code: "Duplicated-success-204",
                        target: response.type,
                    });
                }
                success204Response = convert2CMDHttpResponse(context, response, ["204"], false);
            }
            // remove 202 and 204 from statusCodes
            statusCodes = statusCodes.filter((code) => code !== "202" && code !== "204");
            if (statusCodes.length > 0) {
                if (success2xxResponse !== undefined) {
                    success2xxResponse.statusCode = [
                        ...success2xxResponse.statusCode,
                        ...statusCodes.map((code) => Number(code)),
                    ];
                    context.tracer.trace("AppendSuccess2xxStatusCodes", JSON.stringify(success2xxResponse.statusCode));
                }
                else {
                    success2xxResponse = convert2CMDHttpResponse(context, response, statusCodes, false);
                }
            }
        }
        else if (isRedirect) {
            if (redirectResponse !== undefined) {
                reportDiagnostic(context.program, {
                    code: "Duplicated-redirect",
                    target: response.type,
                });
            }
            redirectResponse = convert2CMDHttpResponse(context, response, statusCodes, false);
        }
        else if (isError) {
            errorResponses.push(convert2CMDHttpResponse(context, response, statusCodes, true));
        }
    }
    const responses = [];
    if (success2xxResponse !== undefined) {
        responses.push(success2xxResponse);
    }
    if (success202Response !== undefined) {
        responses.push(success202Response);
    }
    if (success204Response !== undefined) {
        responses.push(success204Response);
    }
    const success_status_code = [
        ...success2xxResponse?.statusCode || [],
        ...success202Response?.statusCode || [],
        ...success204Response?.statusCode || [],
    ];
    const lro_base_status_code = success_status_code.filter(code => [200, 201].includes(code));
    if (lro_base_status_code.length === 0 && lroMetadata !== undefined && operation.verb === "delete") {
        const lro_response = {
            statusCode: [200, 201],
            isError: false,
            description: "Response schema for long-running operation."
        };
        responses.push(lro_response);
    }
    if (redirectResponse !== undefined) {
        responses.push(redirectResponse);
    }
    responses.push(...errorResponses);
    if (lroMetadata !== undefined && lroMetadata.logicalResult) ;
    return responses;
}
function convert2CMDHttpResponse(context, response, statusCodes, isError) {
    const res = {
        statusCode: statusCodes?.map((code) => Number(code)),
        isError: isError ? true : undefined,
        description: response.description ?? getResponseDescriptionForStatusCodes(statusCodes),
    };
    const contentTypes = [];
    let body;
    for (const data of response.responses) {
        if (data.headers && Object.keys(data.headers).length > 0) {
            res.header ??= {
                items: [],
            };
            for (const name of Object.keys(data.headers)) {
                res.header.items.push({ name });
            }
        }
        if (data.body) {
            if (body && body.type !== data.body.type) {
                reportDiagnostic(context.program, {
                    code: "duplicate-body-types",
                    target: response.type,
                });
            }
            body = data.body;
            contentTypes.push(...data.body.contentTypes);
        }
    }
    if (body) {
        const isBinary = contentTypes.every((t) => isBinaryPayload(body.type, t));
        if (isBinary) {
            throw new Error("NotImplementedError: Binary response are not supported.");
        }
        if (body.bodyKind === "multipart") {
            throw new Error("NotImplementedError: Multipart form data responses are not supported.");
        }
        let schema;
        if (isError) {
            const errorFormat = classifyErrorFormat(context, body.type);
            if (errorFormat === undefined) {
                throw new Error("Error response schema is not supported yet.");
            }
            schema = {
                readOnly: true,
                type: `@${errorFormat}`,
            };
        }
        else {
            schema = convert2CMDSchemaBase({
                ...buildSchemaEmitterContext(context, body.type, "body"),
                visibility: Visibility.Read,
            }, body.type);
        }
        if (!schema) {
            throw new Error("Invalid Response Schema. It's None.");
        }
        res.body = {
            json: {
                schema: schema,
            }
        };
    }
    return res;
}
// Schema functions
function buildSchemaEmitterContext(context, param, type) {
    let collectionFormat;
    if (type === "query") {
        collectionFormat = getQueryParamOptions(context.program, param).format;
    }
    else if (type === "header") {
        collectionFormat = getHeaderFieldOptions(context.program, param).format;
    }
    if (collectionFormat === "csv") {
        collectionFormat = undefined;
    }
    return {
        ...context,
        collectionFormat,
        supportClsSchema: true,
    };
}
function convert2CMDSchema(context, param, name) {
    if (isNeverType(param.type)) {
        return undefined;
    }
    let schema;
    switch (param.type.kind) {
        case "Intrinsic":
            schema = undefined;
            break;
        case "Model":
            schema = convert2CMDSchemaBase(context, param.type);
            break;
        case "ModelProperty":
            schema = convert2CMDSchema(context, param.type);
            break;
        case "Scalar":
            schema = convert2CMDSchemaBase(context, param.type);
            break;
        case "UnionVariant":
            schema = convert2CMDSchemaBase(context, param.type.type);
            break;
        case "Union":
            schema = convert2CMDSchemaBase(context, param.type);
            break;
        case "Enum":
            schema = convert2CMDSchemaBase(context, param.type);
            break;
        // TODO: handle Literals
        case "Number":
        case "String":
        case "Boolean":
            schema = convert2CMDSchemaBase(context, param.type);
            break;
        // case "Tuple":
        default:
            reportDiagnostic(context.program, { code: "Unsupported-Type", target: param.type });
    }
    if (schema) {
        schema = {
            ...schema,
            name: name ?? param.name,
            description: getDoc(context.program, param),
        };
        if (param.defaultValue) {
            schema.default = {
                value: getDefaultValue(context, param.defaultValue),
            };
        }
    }
    if (schema) {
        schema = {
            ...schema,
            ...applySchemaFormat(context, param, schema)
        };
        schema = {
            ...schema,
            ...applyExtensionsDecorators(context, param, schema)
        };
    }
    return schema;
}
function convert2CMDSchemaBase(context, type) {
    if (isNeverType(type)) {
        return undefined;
    }
    let schema;
    switch (type.kind) {
        case "Intrinsic":
            schema = undefined;
            break;
        case "Scalar":
            schema = convertScalar2CMDSchemaBase(context, type);
            break;
        case "Model":
            if (isArrayModelType(context.program, type)) {
                schema = convertModel2CMDArraySchemaBase(context, type);
            }
            else {
                schema = convertModel2CMDObjectSchemaBase(context, type);
            }
            break;
        case "ModelProperty":
            schema = convert2CMDSchema(context, type.type);
            break;
        case "UnionVariant":
            schema = convert2CMDSchemaBase(context, type.type);
            break;
        case "Union":
            schema = convertUnion2CMDSchemaBase(context, type);
            break;
        case "Enum":
            schema = convertEnum2CMDSchemaBase(context, type);
            break;
        // TODO: handle Literals
        case "Number":
        case "String":
        case "Boolean":
            schema = convertLiteral2CMDSchemaBase(context, type);
            break;
        // case "Tuple":
        default:
            reportDiagnostic(context.program, { code: "Unsupported-Type", target: type });
    }
    if (schema) {
        schema = applySchemaFormat(context, type, schema);
        schema = applyExtensionsDecorators(context, type, schema);
    }
    return schema;
}
function convertModel2CMDObjectSchemaBase(context, model) {
    const payloadModel = context.metadateInfo.getEffectivePayloadType(model, context.visibility);
    if (isArrayModelType(context.program, payloadModel)) {
        return undefined;
    }
    let pending;
    if (context.supportClsSchema) {
        pending = context.pendingSchemas.getOrAdd(payloadModel, context.visibility, () => ({
            type: payloadModel,
            visibility: context.visibility,
            ref: context.refs.getOrAdd(payloadModel, context.visibility, () => new Ref()),
            count: 0,
        }));
        pending.count++;
        if (pending.count > 1) {
            return {
                type: new ClsType(pending),
            };
        }
    }
    // const name = getOpenAPITypeName(context.program, type, context.typeNameOptions);
    let object = {
        type: "object",
        cls: pending?.ref,
    };
    const properties = {};
    // inherit from base model
    if (payloadModel.baseModel) {
        const baseSchema = convert2CMDSchemaBase({
            ...context,
            supportClsSchema: false,
        }, payloadModel.baseModel);
        if (baseSchema) {
            Object.assign(object, baseSchema, { cls: pending?.ref });
        }
        const discriminatorInfo = getDiscriminatorInfo(context, payloadModel);
        if (discriminatorInfo) {
            // directly use child definition instead of polymorphism.
            // So the value for discriminator property is const.
            // filter prop in object.props by discriminatorInfo.propertyName and set its const value
            const prop = object.props.find((prop) => prop.name === discriminatorInfo.propertyName);
            prop.const = true;
            prop.default = {
                value: discriminatorInfo.value,
            };
            object.discriminators = undefined;
        }
        if (object.props) {
            for (const prop of object.props) {
                properties[prop.name] = prop;
            }
            object.props = undefined;
        }
    }
    const discriminator = getDiscriminator(context.program, payloadModel);
    for (const prop of payloadModel.properties.values()) {
        if (isNeverType(prop.type)) {
            // If the property has a type of 'never', don't include it in the schema
            continue;
        }
        if (!context.metadateInfo.isPayloadProperty(prop, context.visibility)) {
            continue;
        }
        const jsonName = getJsonName(context, prop);
        let schema = convert2CMDSchema({
            ...context,
            supportClsSchema: true,
        }, prop, jsonName);
        if (schema) {
            if (!context.metadateInfo.isOptional(prop, context.visibility) || prop.name === discriminator?.propertyName) {
                schema.required = true;
            }
            if (isReadonlyProperty(context.program, prop)) {
                schema.readOnly = true;
                if (schema.required) {
                    // read_only property is not required
                    // console.log("Ignore requirement of the read only property: ", schema.name)
                    schema.required = false;
                }
            }
            if (shouldClientFlatten(context, prop)) {
                if (schema.type === "object") {
                    schema = {
                        ...schema,
                        clientFlatten: true,
                    };
                }
                else if (schema.type instanceof ClsType) {
                    schema = {
                        ...schema,
                        clientFlatten: true,
                    };
                }
            }
            properties[schema.name] = schema;
        }
    }
    if (discriminator) {
        const { propertyName } = discriminator;
        console.assert(object.discriminators === undefined, "Discriminator should be undefined.");
        // Push discriminator into base type, but only if it is not already there
        if (!payloadModel.properties.get(propertyName)) {
            const discriminatorProperty = {
                name: propertyName,
                type: "string",
                required: true,
                description: `Discriminator property for ${payloadModel.name}.`,
            };
            properties[propertyName] = discriminatorProperty;
        }
        const discProperty = properties[propertyName];
        const derivedModels = payloadModel.derivedModels.filter(includeDerivedModel);
        for (const child of derivedModels) {
            const childDiscriminatorValue = getDiscriminatorInfo(context, child);
            if (childDiscriminatorValue) {
                const disc = convertModel2CMDObjectDiscriminator(context, child, childDiscriminatorValue);
                if (disc) {
                    object.discriminators ??= [];
                    object.discriminators.push(disc);
                    discProperty.enum ??= {
                        items: [],
                    };
                    discProperty.enum.items.push({
                        value: childDiscriminatorValue.value,
                    });
                }
            }
        }
    }
    if (isRecordModelType(context.program, payloadModel)) {
        object.additionalProps = {
            item: convert2CMDSchemaBase({
                ...context,
                supportClsSchema: true,
            }, payloadModel.indexer.value),
        };
    }
    if (isAzureResourceOverall(context, payloadModel) && properties.location) {
        properties.location = {
            ...properties.location,
            type: "ResourceLocation"
        };
    }
    if (properties.userAssignedIdentities && properties.type) {
        object = {
            ...object,
            type: "IdentityObject",
        };
    }
    if (Object.keys(properties).length > 0) {
        object.props = Object.values(properties).filter((prop) => !isEmptiedSchema(prop));
        if (object.props.length === 0) {
            object.props = undefined;
        }
    }
    if (pending) {
        pending.schema = object;
    }
    return object;
}
function convertModel2CMDArraySchemaBase(context, model) {
    const payloadModel = context.metadateInfo.getEffectivePayloadType(model, context.visibility);
    if (!isArrayModelType(context.program, payloadModel)) {
        return undefined;
    }
    const item = convert2CMDSchemaBase({
        ...context,
        supportClsSchema: true,
    }, payloadModel.indexer.value);
    if (!item) {
        return undefined;
    }
    const array = {
        type: new ArrayType(item.type),
        item: item,
        identifiers: getExtensions(context.program, payloadModel).get("x-ms-identifiers"),
    };
    return array;
}
function convertModel2CMDObjectDiscriminator(context, model, discriminatorInfo) {
    const object = {
        property: discriminatorInfo.propertyName,
        value: discriminatorInfo.value,
    };
    const payloadModel = context.metadateInfo.getEffectivePayloadType(model, context.visibility);
    const properties = {};
    const discriminator = getDiscriminator(context.program, payloadModel);
    for (const prop of payloadModel.properties.values()) {
        if (isNeverType(prop.type)) {
            // If the property has a type of 'never', don't include it in the schema
            continue;
        }
        if (!context.metadateInfo.isPayloadProperty(prop, context.visibility)) {
            continue;
        }
        const jsonName = getJsonName(context, prop);
        let schema = convert2CMDSchema({
            ...context,
            supportClsSchema: true,
        }, prop, jsonName);
        if (schema) {
            if (isReadonlyProperty(context.program, prop)) {
                schema.readOnly = true;
            }
            if (!context.metadateInfo.isOptional(prop, context.visibility) || prop.name === discriminator?.propertyName) {
                schema.required = true;
            }
            if (shouldClientFlatten(context, prop)) {
                if (schema.type === "object") {
                    schema = {
                        ...schema,
                        clientFlatten: true,
                    };
                }
                else if (schema.type instanceof ClsType) {
                    schema = {
                        ...schema,
                        clientFlatten: true,
                    };
                }
            }
            properties[schema.name] = schema;
        }
    }
    // TODO: handle discriminator.propertyName === discriminatorInfo.propertyName
    if (discriminator && discriminator.propertyName !== discriminatorInfo.propertyName) {
        const { propertyName } = discriminator;
        console.assert(object.discriminators === undefined, "Discriminator should be undefined.");
        // Push discriminator into base type, but only if it is not already there
        if (!payloadModel.properties.get(propertyName)) {
            const discriminatorProperty = {
                name: propertyName,
                type: "string",
                required: true,
                description: `Discriminator property for ${payloadModel.name}.`,
            };
            properties[propertyName] = discriminatorProperty;
        }
        const discProperty = properties[propertyName];
        const derivedModels = payloadModel.derivedModels.filter(includeDerivedModel);
        for (const child of derivedModels) {
            const childDiscriminatorValue = getDiscriminatorInfo(context, child);
            if (childDiscriminatorValue) {
                const disc = convertModel2CMDObjectDiscriminator(context, child, childDiscriminatorValue);
                if (disc) {
                    object.discriminators ??= [];
                    object.discriminators.push(disc);
                    discProperty.enum ??= {
                        items: [],
                    };
                    discProperty.enum.items.push({
                        value: childDiscriminatorValue.value,
                    });
                }
            }
        }
    }
    if (Object.keys(properties).length > 0) {
        object.props = Object.values(properties).filter((prop) => !isEmptiedSchema(prop));
        if (object.props.length === 0) {
            object.props = undefined;
        }
    }
    return object;
}
function convertScalar2CMDSchemaBase(context, scalar) {
    const isStd = context.program.checker.isStdType(scalar);
    const encodeData = getEncode(context.program, scalar);
    let schema;
    if (isStd) {
        switch (scalar.name) {
            case "bytes":
                schema = {
                    type: "byte",
                };
                break;
            case "numeric":
                schema = {
                    type: "integer",
                };
                break;
            case "integer":
                schema = {
                    type: "integer",
                };
                break;
            case "int8":
                // TODO: add format for int8
                schema = {
                    type: "integer",
                };
                break;
            case "int16":
                // TODO: add format for int16
                schema = {
                    type: "integer",
                };
                break;
            case "int32":
                schema = {
                    type: "integer32",
                };
                break;
            case "int64":
                schema = {
                    type: "integer64",
                };
                break;
            case "safeint":
                schema = {
                    type: "integer64",
                };
                break;
            case "uint8":
                // TODO: add format for uint8
                schema = {
                    type: "integer",
                };
                break;
            case "uint16":
                // TODO: add format for uint16
                schema = {
                    type: "integer",
                };
                break;
            case "uint32":
                // TODO: add format for uint32
                schema = {
                    type: "integer",
                };
                break;
            case "uint64":
                // TODO: add format for uint64
                schema = {
                    type: "integer",
                };
                break;
            case "float":
                schema = {
                    type: "float",
                };
                break;
            case "float32":
                schema = {
                    type: "float32",
                };
                break;
            case "float64":
                schema = {
                    type: "float64",
                };
                break;
            case "decimal":
                schema = {
                    type: "float64",
                };
                break;
            case "decimal128":
                // TODO: add format for decimal128
                schema = {
                    type: "float",
                };
                break;
            case "string":
                schema = {
                    type: "string",
                };
                break;
            case "url":
                schema = {
                    type: "string",
                };
                break;
            case "plainDate":
                schema = {
                    type: "date",
                };
                break;
            case "plainTime":
                schema = {
                    type: "time",
                };
                break;
            case "utcDateTime":
            case "offsetDateTime":
                switch (encodeData?.encoding) {
                    case "rfc3339":
                        schema = { type: "dateTime" };
                        break;
                    case "unixTimestamp":
                        // TODO: add "unixtime" support
                        schema = { type: "dateTime" };
                        break;
                    case "rfc7231":
                        // TODO: add "date-time-rfc7231" support
                        schema = { type: "dateTime" };
                        break;
                    default:
                        if (encodeData !== undefined) {
                            schema = convertScalar2CMDSchemaBase(context, encodeData.type);
                        }
                        schema ??= { type: "dateTime" };
                }
                break;
            case "duration":
                switch (encodeData?.encoding) {
                    case "ISO8601":
                        schema = { type: "duration" };
                        break;
                    case "seconds":
                        // TODO: add "seconds" support
                        schema = { type: "duration" };
                        break;
                    default:
                        if (encodeData !== undefined) {
                            schema = convertScalar2CMDSchemaBase(context, encodeData.type);
                        }
                        schema ??= { type: "duration" };
                }
                break;
            case "boolean":
                schema = { type: "boolean" };
                break;
        }
    }
    else if (scalar.baseScalar) {
        schema = convertScalar2CMDSchemaBase(context, scalar.baseScalar);
    }
    return schema;
}
function convertUnion2CMDSchemaBase(context, union) {
    const nonNullOptions = [...union.variants.values()]
        .map((x) => x.type)
        .filter((t) => !isNullType(t));
    const nullable = union.variants.size !== nonNullOptions.length;
    if (nonNullOptions.length === 0) {
        reportDiagnostic(context.program, { code: "union-null", target: union });
        return undefined;
    }
    let schema;
    if (nonNullOptions.length === 1) {
        const type = nonNullOptions[0];
        schema = {
            ...convert2CMDSchemaBase(context, type),
            nullable: nullable ? true : undefined,
        };
    }
    else {
        const [asEnum] = getUnionAsEnum(union);
        if (asEnum) {
            schema = convertUnionEnum2CMDSchemaBase(context, union, asEnum);
        }
        else {
            reportDiagnostic(context.program, {
                code: "union-unsupported",
                target: union,
            });
        }
    }
    return schema;
}
function convertUnionEnum2CMDSchemaBase(context, union, e) {
    let schema;
    if (e.kind === 'number') {
        schema = {
            type: "integer",
            nullable: e.nullable ? true : undefined,
            enum: {
                items: Array.from(e.flattenedMembers.values()).map((member) => {
                    return {
                        value: member.value,
                    };
                }),
            }
        };
    }
    else if (e.kind === 'string') {
        schema = {
            type: "string",
            nullable: e.nullable ? true : undefined,
            enum: {
                items: Array.from(e.flattenedMembers.values()).map((member) => {
                    return {
                        value: member.value,
                    };
                }),
            }
        };
    }
    // TODO: handle e.open which supports additional enum values
    return schema;
}
function convertEnum2CMDSchemaBase(context, e) {
    let schema;
    const type = getEnumMemberType(e.members.values().next().value);
    for (const option of e.members.values()) {
        if (type !== getEnumMemberType(option)) {
            return undefined;
        }
    }
    if (type === 'number') {
        schema = {
            type: "integer",
            enum: {
                items: Array.from(e.members.values()).map((member) => {
                    return {
                        value: member.value,
                    };
                }),
            }
        };
    }
    else if (type === 'string') {
        schema = {
            type: "string",
            enum: {
                items: Array.from(e.members.values()).map((member) => {
                    return {
                        value: (member.value ?? member.name),
                    };
                }),
            }
        };
    }
    return schema;
    function getEnumMemberType(member) {
        if (typeof member.value === "number") {
            return "number";
        }
        return "string";
    }
}
function shouldClientFlatten(context, target) {
    return !!(shouldFlattenProperty(context.sdkContext, target) || getExtensions(context.program, target).get("x-ms-client-flatten"));
}
function includeDerivedModel(model) {
    return (!isTemplateDeclaration(model) &&
        (model.templateMapper?.args === undefined ||
            model.templateMapper?.args.length === 0 ||
            model.derivedModels.length > 0));
}
function getDiscriminatorInfo(context, model) {
    let discriminator;
    let current = model;
    while (current.baseModel) {
        discriminator = getDiscriminator(context.program, current.baseModel);
        if (discriminator) {
            break;
        }
        current = current.baseModel;
    }
    if (discriminator === undefined) {
        return undefined;
    }
    const prop = getProperty(model, discriminator.propertyName);
    if (prop) {
        const values = getStringValues(prop.type);
        if (values.length === 1) {
            return { propertyName: discriminator.propertyName, value: values[0] };
        }
    }
    return undefined;
}
function isAzureResourceOverall(context, model) {
    let current = model;
    let isResource = isAzureResource(context.program, current);
    while (!isResource && current.baseModel) {
        current = current.baseModel;
        isResource = isAzureResource(context.program, current);
    }
    return !!isResource;
}
function convertLiteral2CMDSchemaBase(context, type) {
    switch (type.kind) {
        case "Number":
            if (type.numericValue.isInteger) {
                return {
                    type: "integer",
                    enum: {
                        items: [{ value: type.value }]
                    }
                };
            }
            else {
                return {
                    type: "float",
                    enum: {
                        items: [{ value: type.value }]
                    }
                };
            }
        case "String":
            return {
                type: "string",
                enum: {
                    items: [{ value: type.value }]
                }
            };
        case "Boolean":
            return {
                type: "boolean"
            };
        default:
            return undefined;
    }
}
// Return any string literal values for type
function getStringValues(type) {
    switch (type.kind) {
        case "String":
            return [type.value];
        case "Union":
            return [...type.variants.values()].flatMap((x) => getStringValues(x.type)).filter((x) => x);
        case "EnumMember":
            return typeof type.value !== "number" ? [type.value ?? type.name] : [];
        case "UnionVariant":
            return getStringValues(type.type);
        default:
            return [];
    }
}
function processPendingSchemas(context, verbVisibility, suffix) {
    for (const type of context.pendingSchemas.keys()) {
        const group = context.pendingSchemas.get(type);
        for (const visibility of group.keys()) {
            const pending = context.pendingSchemas.get(type).get(visibility);
            if (pending.count < 2) {
                pending.ref.value = undefined;
            }
            else {
                let name = getOpenAPITypeName(context.program, type, context.typeNameOptions);
                if (group.size > 1 && visibility !== Visibility.Read) {
                    // TODO: handle item
                    name += getVisibilitySuffix(verbVisibility, Visibility.Read);
                }
                if (Visibility.Read !== visibility) {
                    name += '_' + suffix;
                }
                else {
                    name += '_read';
                }
                pending.ref.value = name;
            }
        }
    }
}
function isEmptiedSchema(schema) {
    if (!schema.required) {
        if (schema.type === "object") {
            const objectSchema = schema;
            if (!objectSchema.additionalProps && !objectSchema.props && !objectSchema.discriminators && !objectSchema.nullable) {
                return true;
            }
        }
        else if (schema.type instanceof ArrayType) {
            const arraySchema = schema;
            if (!arraySchema.item && !arraySchema.nullable) {
                return true;
            }
        }
    }
    return false;
}
// format functions
function applySchemaFormat(context, type, target) {
    let schema = target;
    const formatStr = getFormat(context.program, type);
    switch (target.type) {
        case "byte":
            schema = {
                ...schema,
                format: emitStringFormat(context, type, schema.format),
            };
            break;
        case "integer":
            schema = {
                ...schema,
                format: emitIntegerFormat(context, type, schema.format),
            };
            break;
        case "integer32":
            schema = {
                ...schema,
                format: emitIntegerFormat(context, type, schema.format),
            };
            break;
        case "integer64":
            schema = {
                ...schema,
                format: emitIntegerFormat(context, type, schema.format),
            };
            break;
        case "float":
            schema = {
                ...schema,
                format: emitFloatFormat(context, type, schema.format),
            };
            break;
        case "float32":
            schema = {
                ...schema,
                format: emitFloatFormat(context, type, schema.format),
            };
            break;
        case "float64":
            schema = {
                ...schema,
                format: emitFloatFormat(context, type, schema.format),
            };
            break;
        case "ResourceId":
            schema = {
                ...schema,
                type: "ResourceId",
                format: emitResourceIdFormat(context, type, schema.format),
            };
            break;
        case "string":
            switch (formatStr) {
                case "uuid":
                    schema = {
                        ...schema,
                        type: "uuid",
                        format: emitStringFormat(context, type, schema.format),
                    };
                    break;
                case "password":
                    schema = {
                        ...schema,
                        type: "password",
                        format: emitStringFormat(context, type, schema.format),
                    };
                    break;
                // TODO: add certificate supports
                case "arm-id":
                    schema = {
                        ...schema,
                        type: "ResourceId",
                        format: emitResourceIdFormat(context, type, undefined),
                    };
                    break;
                case "date":
                    schema = {
                        ...schema,
                        type: "date",
                        format: emitStringFormat(context, type, schema.format),
                    };
                    break;
                case "date-time":
                    schema = {
                        ...schema,
                        type: "date-time",
                        format: emitStringFormat(context, type, schema.format),
                    };
                    break;
                case "date-time-rfc1123":
                    // TODO: add "date-time-rfc1123" support
                    schema = {
                        ...schema,
                        type: "date-time",
                        format: emitStringFormat(context, type, schema.format),
                    };
                    break;
                case "date-time-rfc7231":
                    // TODO: add "date-time-rfc7231" support
                    schema = {
                        ...schema,
                        type: "date-time",
                        format: emitStringFormat(context, type, schema.format),
                    };
                    break;
                case "duration":
                    schema = {
                        ...schema,
                        type: "duration",
                        format: emitStringFormat(context, type, schema.format),
                    };
                    break;
                default:
                    schema = {
                        ...schema,
                        format: emitStringFormat(context, type, schema.format),
                    };
            }
            break;
        // case "date":
        // case "time":
        // case "dateTime":
        // case "duration":
        // case "boolean":
        case "object":
            schema = {
                ...schema,
                format: emitObjectFormat(context, type, schema.format),
            };
            break;
        default:
            if (schema.type instanceof ArrayType) {
                schema = {
                    ...schema,
                    format: emitArrayFormat(context, type, schema.format),
                };
            }
    }
    return schema;
}
function emitStringFormat(context, type, targetFormat) {
    let format = targetFormat;
    const pattern = getPattern(context.program, type);
    if (pattern !== undefined) {
        format = {
            ...format ?? {},
            pattern,
        };
    }
    const maxLength = getMaxLength(context.program, type);
    if (maxLength !== undefined) {
        format = {
            ...format ?? {},
            maxLength,
        };
    }
    const minLength = getMinLength(context.program, type);
    if (minLength !== undefined) {
        format = {
            ...format ?? {},
            minLength,
        };
    }
    return format;
}
function emitResourceIdFormat(context, type, targetFormat) {
    // TODO:
    let format = targetFormat;
    const ext = getArmResourceIdentifierConfig(context.program, type);
    if (ext && ext.allowedResources.length === 1) {
        const type = ext.allowedResources[0].type;
        const scopes = ext.allowedResources[0].scopes ?? ["ResourceGroup"];
        if (scopes.length === 1) {
            switch (scopes[0]) {
                case "ResourceGroup":
                    format = {
                        template: "/subscriptions/{}/resourceGroups/{}/providers/" + type + "/{}",
                    };
                    break;
                case "Subscription":
                    format = {
                        template: "/subscriptions/{}/providers/" + type + "/{}",
                    };
                    break;
                case "ManagementGroup":
                    return {
                        template: "/providers/Microsoft.Management/managementGroups/{}/providers/" + type + "/{}",
                    };
            }
        }
    }
    return format;
}
function emitIntegerFormat(context, type, targetFormat) {
    let format = targetFormat;
    const maximum = getMaxValue(context.program, type);
    if (maximum !== undefined) {
        format = {
            ...format ?? {},
            maximum,
        };
    }
    const minimum = getMinValue(context.program, type);
    if (minimum !== undefined) {
        format = {
            ...format ?? {},
            minimum,
        };
    }
    const multipleOf = getMultipleOf(context.program, type);
    if (multipleOf !== undefined) {
        format = {
            ...format ?? {},
            multipleOf,
        };
    }
    return format;
}
function emitFloatFormat(context, type, targetFormat) {
    let format = targetFormat;
    const maximum = getMaxValue(context.program, type);
    if (maximum !== undefined) {
        format = {
            ...format ?? {},
            maximum,
        };
    }
    const minimum = getMinValue(context.program, type);
    if (minimum !== undefined) {
        format = {
            ...format ?? {},
            minimum,
        };
    }
    const minValueExclusive = getMinValueExclusive(context.program, type);
    if (minValueExclusive !== undefined) {
        format = {
            ...format ?? {},
            minimum: minValueExclusive,
            exclusiveMinimum: true,
        };
    }
    const maxValueExclusive = getMaxValueExclusive(context.program, type);
    if (maxValueExclusive !== undefined) {
        format = {
            ...format ?? {},
            maximum: maxValueExclusive,
            exclusiveMaximum: true,
        };
    }
    const multipleOf = getMultipleOf(context.program, type);
    if (multipleOf !== undefined) {
        format = {
            ...format ?? {},
            multipleOf,
        };
    }
    return format;
}
function emitObjectFormat(context, type, targetFormat) {
    let format = targetFormat;
    const maxProperties = getMaxProperties(context.program, type);
    if (maxProperties !== undefined) {
        format = {
            ...format ?? {},
            maxProperties,
        };
    }
    const minProperties = getMinProperties(context.program, type);
    if (minProperties !== undefined) {
        format = {
            ...format ?? {},
            minProperties,
        };
    }
    return format;
}
function emitArrayFormat(context, type, targetFormat) {
    let format = targetFormat;
    const maxLength = getMaxItems(context.program, type);
    if (maxLength !== undefined) {
        format = {
            ...format ?? {},
            maxLength,
        };
    }
    const minLength = getMinItems(context.program, type);
    if (minLength !== undefined) {
        format = {
            ...format ?? {},
            minLength,
        };
    }
    const uniqueItems = getUniqueItems(context.program, type);
    if (uniqueItems !== undefined) {
        format = {
            ...format ?? {},
            unique: true,
        };
    }
    if (context.collectionFormat !== undefined) {
        format = {
            ...format ?? {},
            strFormat: context.collectionFormat,
        };
    }
    return format;
}
// TODO: add emitResourceIdFormat
// apply extension decorators
function applyExtensionsDecorators(context, type, schema) {
    const extensions = getExtensions(context.program, type);
    if (extensions.has("x-ms-identifiers") && schema.type instanceof ArrayType) {
        schema.identifiers = extensions.get("x-ms-identifiers");
    }
    if (extensions.has("x-ms-secret")) {
        schema.secret = extensions.get("x-ms-secret");
    }
    return schema;
}
// Utils functions
function getJsonName(context, type) {
    const viaProjection = getProjectedName(context.program, type, "json");
    const encodedName = resolveEncodedName(context.program, type, "application/json");
    // Pick the value set via `encodedName` or default back to the legacy projection otherwise.
    // `resolveEncodedName` will return the original name if no @encodedName so we have to do that check
    return encodedName === type.name ? viaProjection ?? type.name : encodedName;
}
function getPathWithoutQuery(path) {
    // strip everything from the key including and after the ?
    return path.replace(/\/?\?.*/, "");
}
function parseNextLinkName(paged) {
    const pathComponents = paged.nextLinkSegments;
    if (pathComponents) {
        return pathComponents[pathComponents.length - 1];
    }
    return undefined;
}
function extractPagedMetadataNested(program, type) {
    // This only works for `is Page<T>` not `extends Page<T>`.
    let paged = getPagedResult(program, type);
    if (paged) {
        return paged;
    }
    if (type.baseModel) {
        paged = getPagedResult(program, type.baseModel);
    }
    if (paged) {
        return paged;
    }
    const templateArguments = type.templateMapper;
    if (templateArguments) {
        for (const argument of templateArguments.args) {
            const modelArgument = argument;
            if (modelArgument) {
                paged = extractPagedMetadataNested(program, modelArgument);
                if (paged) {
                    return paged;
                }
            }
        }
    }
    return paged;
}
function extractPagedMetadata(program, operation) {
    for (const response of operation.responses) {
        const paged = extractPagedMetadataNested(program, response.type);
        if (paged) {
            let nextLinkName = parseNextLinkName(paged);
            if (!nextLinkName) {
                nextLinkName = 'nextLink';
            }
            return {
                nextLinkName,
            };
        }
    }
}
function getModelOrScalarTypeIfNullable(type) {
    if (type.kind === "Model" || type.kind === "Scalar") {
        return type;
    }
    else if (type.kind === "Union") {
        // Remove all `null` types and make sure there's a single model type
        const nonNulls = [...type.variants.values()]
            .map((x) => x.type)
            .filter((variant) => !isNullType(variant));
        if (nonNulls.every((t) => t.kind === "Model" || t.kind === "Scalar")) {
            return nonNulls.length === 1 ? nonNulls[0] : undefined;
        }
    }
    return undefined;
}
function isBinaryPayload(body, contentType) {
    const types = new Set(typeof contentType === "string" ? [contentType] : contentType);
    return (body.kind === "Scalar" &&
        body.name === "bytes" &&
        !types.has("application/json") &&
        !types.has("text/plain"));
}
function getOpenAPI2StatusCodes(context, statusCodes, diagnosticTarget) {
    if (statusCodes === "*") {
        return ["default"];
    }
    else if (typeof statusCodes === "number") {
        return [String(statusCodes)];
    }
    else {
        return rangeToOpenAPI(context, statusCodes, diagnosticTarget);
    }
}
function rangeToOpenAPI(context, range, diagnosticTarget) {
    const reportInvalid = () => reportDiagnostic(context.program, {
        code: "unsupported-status-code-range",
        format: { start: String(range.start), end: String(range.end) },
        target: diagnosticTarget,
    });
    const codes = [];
    let start = range.start;
    let end = range.end;
    if (range.start < 100) {
        reportInvalid();
        start = 100;
        codes.push("default");
    }
    else if (range.end > 599) {
        reportInvalid();
        codes.push("default");
        end = 599;
    }
    const groups = [1, 2, 3, 4, 5];
    for (const group of groups) {
        if (start > end) {
            break;
        }
        const groupStart = group * 100;
        const groupEnd = groupStart + 99;
        if (start >= groupStart && start <= groupEnd) {
            codes.push(`${group}XX`);
            if (start !== groupStart || end < groupEnd) {
                reportInvalid();
            }
            start = groupStart + 100;
        }
    }
    return codes;
}
function getResponseDescriptionForStatusCodes(statusCodes) {
    if (!statusCodes || statusCodes.length === 0) {
        return undefined;
    }
    if (statusCodes.includes("default")) {
        return undefined;
    }
    return getStatusCodeDescription(statusCodes[0]) ?? undefined;
}
function classifyErrorFormat(context, type) {
    // In order to not effect the normal schema's cls reference count, create the new context
    let schema = convert2CMDSchemaBase({
        ...context,
        pendingSchemas: new TwoLevelMap(),
        refs: new TwoLevelMap(),
        visibility: Visibility.Read,
        supportClsSchema: true,
    }, type);
    if (schema === undefined) {
        return undefined;
    }
    if (schema.type instanceof ClsType) {
        schema = getClsDefinitionModel(schema);
    }
    if (schema.type !== "object" || schema.props === undefined) {
        return undefined;
    }
    let errorSchema = schema;
    const props = {};
    for (const prop of errorSchema.props) {
        props[prop.name] = prop;
    }
    if (props.error) {
        if (props.error.type instanceof ClsType) {
            errorSchema = getClsDefinitionModel(props.error);
        }
        else if (props.error.type !== "object") {
            return undefined;
        }
        errorSchema = props.error;
    }
    const propKeys = new Set();
    for (const prop of errorSchema.props) {
        propKeys.add(prop.name);
    }
    if (!(propKeys.has("code") && propKeys.has("message"))) {
        return undefined;
    }
    // difference update propKeys with ["code", "message", "target", "details", "innerError", "innererror"]
    for (const key of ["code", "message", "target", "details", "innerError", "innererror"]) {
        propKeys.delete(key);
    }
    if (propKeys.size === 0) {
        return "ODataV4Format";
    }
    if (propKeys.size === 1 && propKeys.has("additionalInfo")) {
        return "MgmtErrorFormat";
    }
    return undefined;
}
function getClsDefinitionModel(schema) {
    return schema.type.pendingSchema.schema;
}
function getDefaultValue(content, defaultType) {
    switch (defaultType.valueKind) {
        case "StringValue":
            return defaultType.value;
        case "NumericValue":
            return defaultType.value.asNumber() ?? undefined;
        case "BooleanValue":
            return defaultType.value;
        case "ArrayValue":
            return defaultType.values.map((x) => getDefaultValue(content, x));
        case "NullValue":
            return null;
        case "EnumValue":
            return defaultType.value.value ?? defaultType.value.name;
        default:
            reportDiagnostic(content.program, {
                code: "invalid-default",
                format: { type: defaultType.valueKind },
                target: defaultType,
            });
    }
}

async function $onEmit(context) {
    if (context.options.operation === "list-resources") {
        const emitter = createListResourceEmitter(context);
        const resources = await emitter.listResources();
        await emitFile(context.program, {
            path: resolvePath(context.emitterOutputDir, "resources.json"),
            content: JSON.stringify(resources, null, 2),
        });
    }
    else if (context.options.operation === "get-resources-operations") {
        const emitter = await createGetResourceOperationEmitter(context);
        const res = await emitter.getResourcesOperations();
        await emitFile(context.program, {
            path: resolvePath(context.emitterOutputDir, "resources_operations.json"),
            content: JSON.stringify(res, null, 2),
        });
    }
    else {
        throw TypeError(`Unknown operation: ${context.options.operation}`);
    }
}
function createListResourceEmitter(context) {
    const _resources = {};
    const resourceVersions = {};
    async function listResources() {
        const services = listServices(context.program);
        if (services.length === 0) {
            services.push({ type: context.program.getGlobalNamespaceType() });
        }
        for (const service of services) {
            const versions = buildVersionProjections(context.program, service.type);
            for (const record of versions) {
                let program = context.program;
                if (record.projections.length > 0) {
                    program = projectProgram(context.program, record.projections);
                }
                const httpService = ignoreDiagnostics(getAllHttpServices(program))[0];
                emitService(httpService, program, record.version);
            }
        }
        // const tracer = getTracer(context.program);
        // tracer.trace("Resources", JSON.stringify(_resources, null, 2));
        const result = Object.entries(resourceVersions).map(([id, versions]) => ({ id, versions: Object.entries(versions).map(([version, path]) => ({ version, path, id })) }));
        return result;
    }
    return { listResources };
    function emitService(service, program, version) {
        const routes = service.operations;
        reportIfNoRoutes(program, routes);
        routes.forEach((op) => {
            const resourcePath = getResourcePath(program, op);
            const resourceId = swaggerResourcePathToResourceId(resourcePath);
            const versions = resourceVersions[resourceId] || {};
            versions[version] = resourcePath;
            resourceVersions[resourceId] = versions;
            if (!_resources[resourcePath]) {
                _resources[resourcePath] = [];
            }
            _resources[resourcePath].push(`${op.verb}:${version}`);
        });
    }
}
async function createGetResourceOperationEmitter(context) {
    const sdkContext = await createSdkContext(context, "@azure-tools/typespec-aaz");
    const tracer = getTracer(context.program);
    tracer.trace("options", JSON.stringify(context.options, null, 2));
    const apiVersion = sdkContext.apiVersion;
    tracer.trace("apiVersion", apiVersion);
    let projectedProgram;
    const resOps = {};
    context.options?.resources?.forEach((id) => {
        resOps[id] = {
            id: id,
            path: "",
            version: apiVersion
        };
    });
    async function getResourcesOperations() {
        const services = listServices(context.program);
        for (const service of services) {
            // currentService = service;
            const versions = buildVersionProjections(context.program, service.type).filter((v) => apiVersion === v.version);
            for (const record of versions) {
                projectedProgram = context.program;
                if (record.projections.length > 0) {
                    projectedProgram = projectProgram(context.program, record.projections);
                }
                const aazContext = {
                    program: projectedProgram,
                    service: service,
                    sdkContext: sdkContext,
                    apiVersion: apiVersion,
                    tracer,
                };
                emitResourceOps(aazContext);
            }
        }
        const results = [];
        for (const id in resOps) {
            if (resOps[id].pathItem) {
                results.push(resOps[id]);
            }
        }
        return results;
    }
    return { getResourcesOperations };
    function emitResourceOps(context) {
        const services = ignoreDiagnostics(getAllHttpServices(context.program));
        const operations = services[0].operations;
        reportIfNoRoutes(projectedProgram, operations);
        operations.forEach((op) => {
            const resourcePath = getResourcePath(context.program, op);
            const resourceId = swaggerResourcePathToResourceId(resourcePath);
            if (resourceId in resOps) {
                resOps[resourceId].path = resourcePath;
                resOps[resourceId].pathItem = retrieveAAZOperation(context, op, resOps[resourceId].pathItem);
            }
        });
    }
}

var f0 = /*#__PURE__*/Object.freeze({
    __proto__: null,
    $lib: $lib,
    $onEmit: $onEmit
});

const TypeSpecJSSources = {
"dist/src/index.js": f0,
};
const TypeSpecSources = {
  "package.json": "{\"name\":\"@azure-tools/typespec-aaz\",\"version\":\"0.1.0\",\"type\":\"module\",\"tspMain\":\"lib/aaz.tsp\",\"main\":\"dist/src/index.js\",\"exports\":{\".\":{\"types\":\"./dist/src/index.d.ts\",\"default\":\"./dist/src/index.js\"},\"./testing\":{\"types\":\"./dist/src/testing/index.d.ts\",\"default\":\"./dist/src/testing/index.js\"}},\"devDependencies\":{\"@types/node\":\"latest\",\"@typescript-eslint/eslint-plugin\":\"^6.0.0\",\"@typescript-eslint/parser\":\"^6.0.0\",\"@typespec/library-linter\":\"workspace:~\",\"change-case\":\"~5.4.4\",\"eslint\":\"^8.57.0\",\"prettier\":\"^3.0.3\",\"typescript\":\"^5.2.2\"},\"peerDependencies\":{\"@azure-tools/typespec-azure-core\":\"workspace:~\",\"@azure-tools/typespec-client-generator-core\":\"workspace:~\",\"@azure-tools/typespec-azure-resource-manager\":\"workspace:~\",\"@typespec/compiler\":\"workspace:~\",\"@typespec/http\":\"workspace:~\",\"@typespec/json-schema\":\"workspace:~\",\"@typespec/openapi\":\"workspace:~\",\"@typespec/rest\":\"workspace:~\",\"@typespec/versioning\":\"workspace:~\"},\"scripts\":{\"build\":\"tsc -p . && npm run build:tsp\",\"watch\":\"tsc -p . --watch\",\"test\":\"node --test ./dist/test/\",\"build:tsp\":\"tsp compile . --warn-as-error --import @typespec/library-linter --no-emit\",\"lint\":\"eslint src/ test/ --report-unused-disable-directives --max-warnings=0\",\"lint:fix\":\"eslint . --report-unused-disable-directives --fix\",\"format\":\"prettier .  --write\",\"format:check\":\"prettier --check .\"},\"private\":true}",
  "../typespec/core/packages/compiler/lib/intrinsics.tsp": "import \"../dist/src/lib/intrinsic/tsp-index.js\";\nimport \"./prototypes.tsp\";\n\n// This file contains all the intrinsic types of typespec. Everything here will always be loaded\nnamespace TypeSpec;\n\n/**\n * Represent a byte array\n */\nscalar bytes;\n\n/**\n * A numeric type\n */\nscalar numeric;\n\n/**\n * A whole number. This represent any `integer` value possible.\n * It is commonly represented as `BigInteger` in some languages.\n */\nscalar integer extends numeric;\n\n/**\n * A number with decimal value\n */\nscalar float extends numeric;\n\n/**\n * A 64-bit integer. (`-9,223,372,036,854,775,808` to `9,223,372,036,854,775,807`)\n */\nscalar int64 extends integer;\n\n/**\n * A 32-bit integer. (`-2,147,483,648` to `2,147,483,647`)\n */\nscalar int32 extends int64;\n\n/**\n * A 16-bit integer. (`-32,768` to `32,767`)\n */\nscalar int16 extends int32;\n\n/**\n * A 8-bit integer. (`-128` to `127`)\n */\nscalar int8 extends int16;\n\n/**\n * A 64-bit unsigned integer (`0` to `18,446,744,073,709,551,615`)\n */\nscalar uint64 extends integer;\n\n/**\n * A 32-bit unsigned integer (`0` to `4,294,967,295`)\n */\nscalar uint32 extends uint64;\n\n/**\n * A 16-bit unsigned integer (`0` to `65,535`)\n */\nscalar uint16 extends uint32;\n\n/**\n * A 8-bit unsigned integer (`0` to `255`)\n */\nscalar uint8 extends uint16;\n\n/**\n * An integer that can be serialized to JSON (`−9007199254740991 (−(2^53 − 1))` to `9007199254740991 (2^53 − 1)` )\n */\nscalar safeint extends int64;\n\n/**\n * A 64 bit floating point number. (`±5.0 × 10^−324` to `±1.7 × 10^308`)\n */\nscalar float64 extends float;\n\n/**\n * A 32 bit floating point number. (`±1.5 x 10^−45` to `±3.4 x 10^38`)\n */\nscalar float32 extends float64;\n\n/**\n * A decimal number with any length and precision. This represent any `decimal` value possible.\n * It is commonly represented as `BigDecimal` in some languages.\n */\nscalar decimal extends numeric;\n\n/**\n * A 128-bit decimal number.\n */\nscalar decimal128 extends decimal;\n\n/**\n * A sequence of textual characters.\n */\nscalar string;\n\n/**\n * A date on a calendar without a time zone, e.g. \"April 10th\"\n */\nscalar plainDate {\n  /**\n   * Create a plain date from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = plainTime.fromISO(\"2024-05-06\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * A time on a clock without a time zone, e.g. \"3:00 am\"\n */\nscalar plainTime {\n  /**\n   * Create a plain time from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = plainTime.fromISO(\"12:34\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * An instant in coordinated universal time (UTC)\"\n */\nscalar utcDateTime {\n  /**\n   * Create a date from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = utcDateTime.fromISO(\"2024-05-06T12:20-12Z\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * A date and time in a particular time zone, e.g. \"April 10th at 3:00am in PST\"\n */\nscalar offsetDateTime {\n  /**\n   * Create a date from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = offsetDateTime.fromISO(\"2024-05-06T12:20-12-0700\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * A duration/time period. e.g 5s, 10h\n */\nscalar duration {\n  /**\n   * Create a duration from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = duration.fromISO(\"P1Y1D\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * Boolean with `true` and `false` values.\n */\nscalar boolean;\n\n/**\n * @dev Array model type, equivalent to `Element[]`\n * @template Element The type of the array elements\n */\n@indexer(integer, Element)\nmodel Array<Element> {}\n\n/**\n * @dev Model with string properties where all the properties have type `Property`\n * @template Element The type of the properties\n */\n@indexer(string, Element)\nmodel Record<Element> {}\n",
  "../typespec/core/packages/compiler/lib/prototypes.tsp": "namespace TypeSpec.Prototypes;\n\nextern dec getter(target: unknown);\n\nnamespace Types {\n  interface ModelProperty {\n    @getter type(): unknown;\n  }\n\n  interface Operation {\n    @getter returnType(): unknown;\n    @getter parameters(): unknown;\n  }\n\n  interface Array<TElementType> {\n    @getter elementType(): TElementType;\n  }\n}\n",
  "../typespec/core/packages/compiler/lib/std/main.tsp": "// TypeSpec standard library. Everything in here can be omitted by using `--nostdlib` cli flag or `nostdlib` in the config.\nimport \"./types.tsp\";\nimport \"./decorators.tsp\";\nimport \"./reflection.tsp\";\nimport \"./projected-names.tsp\";\nimport \"./visibility.tsp\";\n",
  "../typespec/core/packages/compiler/lib/std/types.tsp": "namespace TypeSpec;\n\n/**\n * Represent a 32-bit unix timestamp datetime with 1s of granularity.\n * It measures time by the number of seconds that have elapsed since 00:00:00 UTC on 1 January 1970.\n */\n@encode(\"unixTimestamp\", int32)\nscalar unixTimestamp32 extends utcDateTime;\n\n/**\n * Represent a model\n */\n// Deprecated June 2023 sprint\n#deprecated \"object is deprecated. Please use {} for an empty model, `Record<unknown>` for a record with unknown property types, `unknown[]` for an array.\"\nmodel object {}\n\n/**\n * Represent a URL string as described by https://url.spec.whatwg.org/\n */\nscalar url extends string;\n\n/**\n * Represents a collection of optional properties.\n *\n * @template Source An object whose spread properties are all optional.\n */\n@doc(\"The template for adding optional properties.\")\n@withOptionalProperties\nmodel OptionalProperties<Source> {\n  ...Source;\n}\n\n/**\n * Represents a collection of updateable properties.\n *\n * @template Source An object whose spread properties are all updateable.\n */\n@doc(\"The template for adding updateable properties.\")\n@withUpdateableProperties\nmodel UpdateableProperties<Source> {\n  ...Source;\n}\n\n/**\n * Represents a collection of omitted properties.\n *\n * @template Source An object whose properties are spread.\n * @template Keys The property keys to omit.\n */\n@doc(\"The template for omitting properties.\")\n@withoutOmittedProperties(Keys)\nmodel OmitProperties<Source, Keys extends string> {\n  ...Source;\n}\n\n/**\n * Represents a collection of properties with only the specified keys included.\n *\n * @template Source An object whose properties are spread.\n * @template Keys The property keys to include.\n */\n@doc(\"The template for picking properties.\")\n@withPickedProperties(Keys)\nmodel PickProperties<Source, Keys extends string> {\n  ...Source;\n}\n\n/**\n * Represents a collection of properties with default values omitted.\n *\n * @template Source An object whose spread property defaults are all omitted.\n */\n@withoutDefaultValues\nmodel OmitDefaults<Source> {\n  ...Source;\n}\n\n/**\n * Applies a visibility setting to a collection of properties.\n *\n * @template Source An object whose properties are spread.\n * @template Visibility The visibility to apply to all properties.\n */\n@doc(\"The template for setting the default visibility of key properties.\")\n@withDefaultKeyVisibility(Visibility)\nmodel DefaultKeyVisibility<Source, Visibility extends valueof string> {\n  ...Source;\n}\n",
  "../typespec/core/packages/compiler/lib/std/decorators.tsp": "import \"../../dist/src/lib/tsp-index.js\";\n\nusing TypeSpec.Reflection;\n\nnamespace TypeSpec;\n\n/**\n * Typically a short, single-line description.\n * @param summary Summary string.\n *\n * @example\n * ```typespec\n * @summary(\"This is a pet\")\n * model Pet {}\n * ```\n */\nextern dec summary(target: unknown, summary: valueof string);\n\n/**\n * Attach a documentation string.\n * @param doc Documentation string\n * @param formatArgs Record with key value pair that can be interpolated in the doc.\n *\n * @example\n * ```typespec\n * @doc(\"Represent a Pet available in the PetStore\")\n * model Pet {}\n * ```\n */\nextern dec doc(target: unknown, doc: valueof string, formatArgs?: {});\n\n/**\n * Attach a documentation string to describe the successful return types of an operation.\n * If an operation returns a union of success and errors it only describes the success. See `@errorsDoc` for error documentation.\n * @param doc Documentation string\n *\n * @example\n * ```typespec\n * @returnsDoc(\"Returns doc\")\n * op get(): Pet | NotFound;\n * ```\n */\nextern dec returnsDoc(target: Operation, doc: valueof string);\n\n/**\n * Attach a documentation string to describe the error return types of an operation.\n * If an operation returns a union of success and errors it only describes the errors. See `@returnsDoc` for success documentation.\n * @param doc Documentation string\n *\n * @example\n * ```typespec\n * @errorsDoc(\"Errors doc\")\n * op get(): Pet | NotFound;\n * ```\n */\nextern dec errorsDoc(target: Operation, doc: valueof string);\n\n/**\n * Mark this type as deprecated.\n *\n * NOTE: This decorator **should not** be used, use the `#deprecated` directive instead.\n *\n * @deprecated Use the `#deprecated` [directive](https://typespec.io/docs/language-basics/directives/#deprecated) instead.\n * @param message Deprecation message.\n *\n * @example\n *\n * Use the `#deprecated` directive instead:\n *\n * ```typespec\n * #deprecated \"Use ActionV2\"\n * op Action<Result>(): Result;\n * ```\n */\n#deprecated \"@deprecated decorator is deprecated. Use the `#deprecated` directive instead.\"\nextern dec deprecated(target: unknown, message: valueof string);\n\n/**\n * Service options.\n */\nmodel ServiceOptions {\n  /**\n   * Title of the service.\n   */\n  title?: string;\n\n  /**\n   * Version of the service.\n   */\n  version?: string;\n}\n\n/**\n * Mark this namespace as describing a service and configure service properties.\n * @param options Optional configuration for the service.\n *\n * @example\n * ```typespec\n * @service\n * namespace PetStore;\n * ```\n *\n * @example Setting service title\n * ```typespec\n * @service({title: \"Pet store\"})\n * namespace PetStore;\n * ```\n *\n * @example Setting service version\n * ```typespec\n * @service({version: \"1.0\"})\n * namespace PetStore;\n * ```\n */\nextern dec service(target: Namespace, options?: ServiceOptions);\n\n/**\n * Specify that this model is an error type. Operations return error types when the operation has failed.\n *\n * @example\n * ```typespec\n * @error\n * model PetStoreError {\n *   code: string;\n *   message: string;\n * }\n * ```\n */\nextern dec error(target: Model);\n\n/**\n * Specify a known data format hint for this string type. For example `uuid`, `uri`, etc.\n * This differs from the `@pattern` decorator which is meant to specify a regular expression while `@format` accepts a known format name.\n * The format names are open ended and are left to emitter to interpret.\n *\n * @param format format name.\n *\n * @example\n * ```typespec\n * @format(\"uuid\")\n * scalar uuid extends string;\n * ```\n */\nextern dec format(target: string | bytes | ModelProperty, format: valueof string);\n\n/**\n * Specify the the pattern this string should respect using simple regular expression syntax.\n * The following syntax is allowed: alternations (`|`), quantifiers (`?`, `*`, `+`, and `{ }`), wildcard (`.`), and grouping parentheses.\n * Advanced features like look-around, capture groups, and references are not supported.\n *\n * This decorator may optionally provide a custom validation _message_. Emitters may choose to use the message to provide\n * context when pattern validation fails. For the sake of consistency, the message should be a phrase that describes in\n * plain language what sort of content the pattern attempts to validate. For example, a complex regular expression that\n * validates a GUID string might have a message like \"Must be a valid GUID.\"\n *\n * @param pattern Regular expression.\n * @param validationMessage Optional validation message that may provide context when validation fails.\n *\n * @example\n * ```typespec\n * @pattern(\"[a-z]+\", \"Must be a string consisting of only lower case letters and of at least one character.\")\n * scalar LowerAlpha extends string;\n * ```\n */\nextern dec pattern(\n  target: string | bytes | ModelProperty,\n  pattern: valueof string,\n  validationMessage?: valueof string\n);\n\n/**\n * Specify the minimum length this string type should be.\n * @param value Minimum length\n *\n * @example\n * ```typespec\n * @minLength(2)\n * scalar Username extends string;\n * ```\n */\nextern dec minLength(target: string | ModelProperty, value: valueof integer);\n\n/**\n * Specify the maximum length this string type should be.\n * @param value Maximum length\n *\n * @example\n * ```typespec\n * @maxLength(20)\n * scalar Username extends string;\n * ```\n */\nextern dec maxLength(target: string | ModelProperty, value: valueof integer);\n\n/**\n * Specify the minimum number of items this array should have.\n * @param value Minimum number\n *\n * @example\n * ```typespec\n * @minItems(1)\n * model Endpoints is string[];\n * ```\n */\nextern dec minItems(target: unknown[] | ModelProperty, value: valueof integer);\n\n/**\n * Specify the maximum number of items this array should have.\n * @param value Maximum number\n *\n * @example\n * ```typespec\n * @maxItems(5)\n * model Endpoints is string[];\n * ```\n */\nextern dec maxItems(target: unknown[] | ModelProperty, value: valueof integer);\n\n/**\n * Specify the minimum value this numeric type should be.\n * @param value Minimum value\n *\n * @example\n * ```typespec\n * @minValue(18)\n * scalar Age is int32;\n * ```\n */\nextern dec minValue(target: numeric | ModelProperty, value: valueof numeric);\n\n/**\n * Specify the maximum value this numeric type should be.\n * @param value Maximum value\n *\n * @example\n * ```typespec\n * @maxValue(200)\n * scalar Age is int32;\n * ```\n */\nextern dec maxValue(target: numeric | ModelProperty, value: valueof numeric);\n\n/**\n * Specify the minimum value this numeric type should be, exclusive of the given\n * value.\n * @param value Minimum value\n *\n * @example\n * ```typespec\n * @minValueExclusive(0)\n * scalar distance is float64;\n * ```\n */\nextern dec minValueExclusive(target: numeric | ModelProperty, value: valueof numeric);\n\n/**\n * Specify the maximum value this numeric type should be, exclusive of the given\n * value.\n * @param value Maximum value\n *\n * @example\n * ```typespec\n * @maxValueExclusive(50)\n * scalar distance is float64;\n * ```\n */\nextern dec maxValueExclusive(target: numeric | ModelProperty, value: valueof numeric);\n\n/**\n * Mark this string as a secret value that should be treated carefully to avoid exposure\n *\n * @example\n * ```typespec\n * @secret\n * scalar Password is string;\n * ```\n */\nextern dec secret(target: string | ModelProperty);\n\n/**\n * Attaches a tag to an operation, interface, or namespace. Multiple `@tag` decorators can be specified to attach multiple tags to a TypeSpec element.\n * @param tag Tag value\n */\nextern dec tag(target: Namespace | Interface | Operation, tag: valueof string);\n\n/**\n * Specifies how a templated type should name their instances.\n * @param name name the template instance should take\n * @param formatArgs Model with key value used to interpolate the name\n *\n * @example\n * ```typespec\n * @friendlyName(\"{name}List\", T)\n * model List<Item> {\n *   value: Item[];\n *   nextLink: string;\n * }\n * ```\n */\nextern dec friendlyName(target: unknown, name: valueof string, formatArgs?: unknown);\n\n/**\n * Provide a set of known values to a string type.\n * @param values Known values enum.\n *\n * @example\n * ```typespec\n * @knownValues(KnownErrorCode)\n * scalar ErrorCode extends string;\n *\n * enum KnownErrorCode {\n *   NotFound,\n *   Invalid,\n * }\n * ```\n */\n#deprecated \"This decorator has been deprecated. Use a named union of string literals with a string variant to achieve the same result without a decorator.\"\nextern dec knownValues(target: string | numeric | ModelProperty, values: Enum);\n\n/**\n * Mark a model property as the key to identify instances of that type\n * @param altName Name of the property. If not specified, the decorated property name is used.\n *\n * @example\n * ```typespec\n * model Pet {\n *   @key id: string;\n * }\n * ```\n */\nextern dec key(target: ModelProperty, altName?: valueof string);\n\n/**\n * Specify this operation is an overload of the given operation.\n * @param overloadbase Base operation that should be a union of all overloads\n *\n * @example\n * ```typespec\n * op upload(data: string | bytes, @header contentType: \"text/plain\" | \"application/octet-stream\"): void;\n * @overload(upload)\n * op uploadString(data: string, @header contentType: \"text/plain\" ): void;\n * @overload(upload)\n * op uploadBytes(data: bytes, @header contentType: \"application/octet-stream\"): void;\n * ```\n */\nextern dec overload(target: Operation, overloadbase: Operation);\n\n/**\n * DEPRECATED: Use `@encodedName` instead.\n *\n * Provide an alternative name for this type.\n * @param targetName Projection target\n * @param projectedName Alternative name\n *\n * @example\n * ```typespec\n * model Certificate {\n *   @projectedName(\"json\", \"exp\")\n *   expireAt: int32;\n * }\n * ```\n */\n#deprecated \"Use `@encodedName` instead for changing the name over the wire.\"\nextern dec projectedName(\n  target: unknown,\n  targetName: valueof string,\n  projectedName: valueof string\n);\n\n/**\n * Provide an alternative name for this type when serialized to the given mime type.\n * @param mimeType Mime type this should apply to. The mime type should be a known mime type as described here https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types without any suffix (e.g. `+json`)\n * @param name Alternative name\n *\n * @example\n *\n * ```typespec\n * model Certificate {\n *   @encodedName(\"application/json\", \"exp\")\n *   @encodedName(\"application/xml\", \"expiry\")\n *   expireAt: int32;\n * }\n * ```\n *\n * @example Invalid values\n *\n * ```typespec\n * @encodedName(\"application/merge-patch+json\", \"exp\")\n *              ^ error cannot use subtype\n * ```\n */\nextern dec encodedName(target: unknown, mimeType: valueof string, name: valueof string);\n\n/**\n * Specify the property to be used to discriminate this type.\n * @param propertyName The property name to use for discrimination\n *\n * @example\n *\n * ```typespec\n * @discriminator(\"kind\")\n * union Pet{ cat: Cat, dog: Dog }\n *\n * model Cat {kind: \"cat\", meow: boolean}\n * model Dog {kind: \"dog\", bark: boolean}\n * ```\n *\n * ```typespec\n * @discriminator(\"kind\")\n * model Pet{ kind: string }\n *\n * model Cat extends Pet {kind: \"cat\", meow: boolean}\n * model Dog extends Pet  {kind: \"dog\", bark: boolean}\n * ```\n */\nextern dec discriminator(target: Model | Union, propertyName: valueof string);\n\n/**\n * Known encoding to use on utcDateTime or offsetDateTime\n */\nenum DateTimeKnownEncoding {\n  /**\n   * RFC 3339 standard. https://www.ietf.org/rfc/rfc3339.txt\n   * Encode to string.\n   */\n  rfc3339: \"rfc3339\",\n\n  /**\n   * RFC 7231 standard. https://www.ietf.org/rfc/rfc7231.txt\n   * Encode to string.\n   */\n  rfc7231: \"rfc7231\",\n\n  /**\n   * Encode a datetime to a unix timestamp.\n   * Unix timestamps are represented as an integer number of seconds since the Unix epoch and usually encoded as an int32.\n   */\n  unixTimestamp: \"unixTimestamp\",\n}\n\n/**\n * Known encoding to use on duration\n */\nenum DurationKnownEncoding {\n  /**\n   * ISO8601 duration\n   */\n  ISO8601: \"ISO8601\",\n\n  /**\n   * Encode to integer or float\n   */\n  seconds: \"seconds\",\n}\n\n/**\n * Known encoding to use on bytes\n */\nenum BytesKnownEncoding {\n  /**\n   * Encode to Base64\n   */\n  base64: \"base64\",\n\n  /**\n   * Encode to Base64 Url\n   */\n  base64url: \"base64url\",\n}\n\n/**\n * Encoding for serializing arrays\n */\nenum ArrayEncoding {\n  /** Each values of the array is separated by a | */\n  pipeDelimited,\n\n  /** Each values of the array is separated by a <space> */\n  spaceDelimited,\n}\n\n/**\n * Specify how to encode the target type.\n * @param encodingOrEncodeAs Known name of an encoding or a scalar type to encode as(Only for numeric types to encode as string).\n * @param encodedAs What target type is this being encoded as. Default to string.\n *\n * @example offsetDateTime encoded with rfc7231\n *\n * ```tsp\n * @encode(\"rfc7231\")\n * scalar myDateTime extends offsetDateTime;\n * ```\n *\n * @example utcDateTime encoded with unixTimestamp\n *\n * ```tsp\n * @encode(\"unixTimestamp\", int32)\n * scalar myDateTime extends unixTimestamp;\n * ```\n *\n * @example encode numeric type to string\n *\n * ```tsp\n * model Pet {\n *   @encode(string) id: int64;\n * }\n * ```\n */\nextern dec encode(\n  target: Scalar | ModelProperty,\n  encodingOrEncodeAs: (valueof string | EnumMember) | Scalar,\n  encodedAs?: Scalar\n);\n\n/** Options for example decorators */\nmodel ExampleOptions {\n  /** The title of the example */\n  title?: string;\n\n  /** Description of the example */\n  description?: string;\n}\n\n/**\n * Provide an example value for a data type.\n *\n * @param example Example value.\n * @param options Optional metadata for the example.\n *\n * @example\n *\n * ```tsp\n * @example(#{name: \"Fluffy\", age: 2})\n * model Pet {\n *  name: string;\n *  age: int32;\n * }\n * ```\n */\nextern dec example(\n  target: Model | Enum | Scalar | Union | ModelProperty | UnionVariant,\n  example: valueof unknown,\n  options?: valueof ExampleOptions\n);\n\n/**\n * Operation example configuration.\n */\nmodel OperationExample {\n  /** Example request body. */\n  parameters?: unknown;\n\n  /** Example response body. */\n  returnType?: unknown;\n}\n\n/**\n * Provide example values for an operation's parameters and corresponding return type.\n *\n * @param example Example value.\n * @param options Optional metadata for the example.\n *\n * @example\n *\n * ```tsp\n * @opExample(#{parameters: #{name: \"Fluffy\", age: 2}, returnType: #{name: \"Fluffy\", age: 2, id: \"abc\"})\n * op createPet(pet: Pet): Pet;\n * ```\n */\nextern dec opExample(\n  target: Operation,\n  example: valueof OperationExample,\n  options?: valueof ExampleOptions\n);\n\n/**\n * Returns the model with required properties removed.\n */\nextern dec withOptionalProperties(target: Model);\n\n/**\n * Returns the model with any default values removed.\n */\nextern dec withoutDefaultValues(target: Model);\n\n/**\n * Returns the model with the given properties omitted.\n * @param omit List of properties to omit\n */\nextern dec withoutOmittedProperties(target: Model, omit: string | Union);\n\n/**\n * Returns the model with only the given properties included.\n * @param pick List of properties to include\n */\nextern dec withPickedProperties(target: Model, pick: string | Union);\n\n//---------------------------------------------------------------------------\n// Paging\n//---------------------------------------------------------------------------\n\n/**\n * Mark this operation as a `list` operation that returns a paginated list of items.\n */\nextern dec list(target: Operation);\n\n/**\n * Pagination property defining the number of items to skip.\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n * }\n * @list op listPets(@offset skip: int32, @pageSize pageSize: int8): Page<Pet>;\n * ```\n */\nextern dec offset(target: ModelProperty);\n\n/**\n * Pagination property defining the page index.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n * }\n * @list op listPets(@pageIndex page: int32, @pageSize pageSize: int8): Page<Pet>;\n * ```\n */\nextern dec pageIndex(target: ModelProperty);\n\n/**\n * Specify the pagination parameter that controls the maximum number of items to include in a page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n * }\n * @list op listPets(@pageIndex page: int32, @pageSize pageSize: int8): Page<Pet>;\n * ```\n */\nextern dec pageSize(target: ModelProperty);\n\n/**\n * Specify the the property that contains the array of page items.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n * }\n * @list op listPets(@pageIndex page: int32, @pageSize pageSize: int8): Page<Pet>;\n * ```\n */\nextern dec pageItems(target: ModelProperty);\n\n/**\n * Pagination property defining the token to get to the next page.\n * It MUST be specified both on the request parameter and the response.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @continuationToken continuationToken: string;\n * }\n * @list op listPets(@continuationToken continuationToken: string): Page<Pet>;\n * ```\n */\nextern dec continuationToken(target: ModelProperty);\n\n/**\n * Pagination property defining a link to the next page.\n *\n * It is expected that navigating to the link will return the same set of responses as the operation that returned the current page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @nextLink next: url;\n *   @prevLink prev: url;\n *   @firstLink first: url;\n *   @lastLink last: url;\n * }\n * @list op listPets(): Page<Pet>;\n * ```\n */\nextern dec nextLink(target: ModelProperty);\n\n/**\n * Pagination property defining a link to the previous page.\n *\n * It is expected that navigating to the link will return the same set of responses as the operation that returned the current page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @nextLink next: url;\n *   @prevLink prev: url;\n *   @firstLink first: url;\n *   @lastLink last: url;\n * }\n * @list op listPets(): Page<Pet>;\n * ```\n */\nextern dec prevLink(target: ModelProperty);\n\n/**\n * Pagination property defining a link to the first page.\n *\n * It is expected that navigating to the link will return the same set of responses as the operation that returned the current page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @nextLink next: url;\n *   @prevLink prev: url;\n *   @firstLink first: url;\n *   @lastLink last: url;\n * }\n * @list op listPets(): Page<Pet>;\n * ```\n */\nextern dec firstLink(target: ModelProperty);\n\n/**\n * Pagination property defining a link to the last page.\n *\n * It is expected that navigating to the link will return the same set of responses as the operation that returned the current page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @nextLink next: url;\n *   @prevLink prev: url;\n *   @firstLink first: url;\n *   @lastLink last: url;\n * }\n * @list op listPets(): Page<Pet>;\n * ```\n */\nextern dec lastLink(target: ModelProperty);\n\n//---------------------------------------------------------------------------\n// Debugging\n//---------------------------------------------------------------------------\n\n/**\n * A debugging decorator used to inspect a type.\n * @param text Custom text to log\n */\nextern dec inspectType(target: unknown, text: valueof string);\n\n/**\n * A debugging decorator used to inspect a type name.\n * @param text Custom text to log\n */\nextern dec inspectTypeName(target: unknown, text: valueof string);\n",
  "../typespec/core/packages/compiler/lib/std/reflection.tsp": "namespace TypeSpec.Reflection;\n\nmodel Enum {}\nmodel EnumMember {}\nmodel Interface {}\nmodel Model {}\nmodel ModelProperty {}\nmodel Namespace {}\nmodel Operation {}\nmodel Scalar {}\nmodel Union {}\nmodel UnionVariant {}\nmodel StringTemplate {}\n",
  "../typespec/core/packages/compiler/lib/std/projected-names.tsp": "// Set of projections consuming the @projectedName decorator\n#suppress \"projections-are-experimental\"\nprojection op#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n  }\n}\n\n#suppress \"projections-are-experimental\"\nprojection interface#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n  }\n}\n\n#suppress \"projections-are-experimental\"\nprojection model#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n\n    self::properties::forEach((p) => {\n      if hasProjectedName(p, targetName) {\n        self::renameProperty(p::name, getProjectedName(p, targetName));\n      };\n    });\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n\n    self::projectionBase::properties::forEach((p) => {\n      if hasProjectedName(p, targetName) {\n        self::renameProperty(getProjectedName(p, targetName), p::name);\n      };\n    });\n  }\n}\n\n#suppress \"projections-are-experimental\"\nprojection enum#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n\n    self::members::forEach((p) => {\n      if hasProjectedName(p, targetName) {\n        self::renameMember(p::name, getProjectedName(p, targetName));\n      };\n    });\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n\n    self::projectionBase::members::forEach((p) => {\n      if hasProjectedName(p, targetName) {\n        self::renameMember(getProjectedName(p, targetName), p::name);\n      };\n    });\n  }\n}\n\n#suppress \"projections-are-experimental\"\nprojection union#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n  }\n}\n",
  "../typespec/core/packages/compiler/lib/std/visibility.tsp": "// Copyright (c) Microsoft Corporation\n// Licensed under the MIT license.\n\nimport \"../../dist/src/lib/tsp-index.js\";\n\nusing TypeSpec.Reflection;\n\nnamespace TypeSpec;\n\n/**\n * Indicates that a property is only considered to be present or applicable (\"visible\") with\n * the in the given named contexts (\"visibilities\"). When a property has no visibilities applied\n * to it, it is implicitly visible always.\n *\n * As far as the TypeSpec core library is concerned, visibilities are open-ended and can be arbitrary\n * strings, but  the following visibilities are well-known to standard libraries and should be used\n * with standard emitters that interpret them as follows:\n *\n * - \"read\": output of any operation.\n * - \"create\": input to operations that create an entity..\n * - \"query\": input to operations that read data.\n * - \"update\": input to operations that update data.\n * - \"delete\": input to operations that delete data.\n *\n * See also: [Automatic visibility](https://typespec.io/docs/libraries/http/operations#automatic-visibility)\n *\n * @param visibilities List of visibilities which apply to this property.\n *\n * @example\n *\n * ```typespec\n * model Dog {\n *   // the service will generate an ID, so you don't need to send it.\n *   @visibility(Lifecycle.Read) id: int32;\n *   // the service will store this secret name, but won't ever return it\n *   @visibility(Lifecycle.Create, Lifecycle.Update) secretName: string;\n *   // the regular name is always present\n *   name: string;\n * }\n * ```\n */\nextern dec visibility(target: ModelProperty, ...visibilities: valueof (string | EnumMember)[]);\n\n/**\n * Indicates that a property is not visible in the given visibility class.\n *\n * This decorator removes all active visibility modifiers from the property within\n * the given visibility class.\n *\n * @param visibilityClass The visibility class to make the property invisible within.\n *\n * @example\n * ```typespec\n * model Example {\n *   @invisible(Lifecycle)\n *   hidden_property: string;\n * }\n * ```\n */\nextern dec invisible(target: ModelProperty, visibilityClass: Enum);\n\n/**\n * Removes visibility modifiers from a property.\n *\n * If the visibility modifiers for a visibility class have not been initialized,\n * this decorator will use the default visibility modifiers for the visibility\n * class as the default modifier set.\n *\n * @param target The property to remove visibility from.\n * @param visibilities The visibility modifiers to remove from the target property.\n *\n * @example\n * ```typespec\n * model Example {\n *   // This property will have the Create and Update visibilities, but not the\n *   // Read visibility, since it is removed.\n *   @removeVisibility(Lifecycle.Read)\n *   secret_property: string;\n * }\n * ```\n */\nextern dec removeVisibility(target: ModelProperty, ...visibilities: valueof EnumMember[]);\n\n/**\n * Removes properties that are not considered to be present or applicable\n * (\"visible\") in the given named contexts (\"visibilities\"). Can be used\n * together with spread to effectively spread only visible properties into\n * a new model.\n *\n * See also: [Automatic visibility](https://typespec.io/docs/libraries/http/operations#automatic-visibility)\n *\n * When using an emitter that applies visibility automatically, it is generally\n * not necessary to use this decorator.\n *\n * @param visibilities List of visibilities which apply to this property.\n *\n * @example\n * ```typespec\n * model Dog {\n *   @visibility(\"read\") id: int32;\n *   @visibility(\"create\", \"update\") secretName: string;\n *   name: string;\n * }\n *\n * // The spread operator will copy all the properties of Dog into DogRead,\n * // and @withVisibility will then remove those that are not visible with\n * // create or update visibility.\n * //\n * // In this case, the id property is removed, and the name and secretName\n * // properties are kept.\n * @withVisibility(\"create\", \"update\")\n * model DogCreateOrUpdate {\n *   ...Dog;\n * }\n *\n * // In this case the id and name properties are kept and the secretName property\n * // is removed.\n * @withVisibility(\"read\")\n * model DogRead {\n *   ...Dog;\n * }\n * ```\n */\nextern dec withVisibility(target: Model, ...visibilities: valueof (string | EnumMember)[]);\n\n/**\n * Set the visibility of key properties in a model if not already set.\n *\n * This will set the visibility modifiers of all key properties in the model if the visibility is not already _explicitly_ set,\n * but will not change the visibility of any properties that have visibility set _explicitly_, even if the visibility\n * is the same as the default visibility.\n *\n * Visibility may be explicitly set using any of the following decorators:\n *\n * - `@visibility`\n * - `@removeVisibility`\n * - `@invisible`\n *\n * @param visibility The desired default visibility value. If a key property already has visibility set, it will not be changed.\n */\nextern dec withDefaultKeyVisibility(target: Model, visibility: valueof string | EnumMember);\n\n/**\n * Sets which visibilities apply to parameters for the given operation.\n *\n * @param visibilities List of visibility strings which apply to this operation.\n */\nextern dec parameterVisibility(target: Operation, ...visibilities: valueof (string | EnumMember)[]);\n\n/**\n * Sets which visibilities apply to the return type for the given operation.\n * @param visibilities List of visibility strings which apply to this operation.\n */\nextern dec returnTypeVisibility(\n  target: Operation,\n  ...visibilities: valueof (string | EnumMember)[]\n);\n\n/**\n * Returns the model with non-updateable properties removed.\n */\nextern dec withUpdateableProperties(target: Model);\n\n/**\n * Declares the default visibility modifiers for a visibility class.\n *\n * The default modifiers are used when a property does not have any visibility decorators\n * applied to it.\n *\n * The modifiers passed to this decorator _MUST_ be members of the target Enum.\n *\n * @param visibilities the list of modifiers to use as the default visibility modifiers.\n */\nextern dec defaultVisibility(target: Enum, ...visibilities: valueof EnumMember[]);\n\n/**\n * A visibility class for resource lifecycle phases.\n *\n * These visibilities control whether a property is visible during the create, read, and update phases of a resource's\n * lifecycle.\n *\n * @example\n * ```typespec\n * model Dog {\n *  @visibility(Lifecycle.Read) id: int32;\n *  @visibility(Lifecycle.Create, Lifecycle.Update) secretName: string;\n *  name: string;\n * }\n * ```\n *\n * In this example, the `id` property is only visible during the read phase, and the `secretName` property is only visible\n * during the create and update phases. This means that the server will return the `id` property when returning a `Dog`,\n * but the client will not be able to set or update it. In contrast, the `secretName` property can be set when creating\n * or updating a `Dog`, but the server will never return it. The `name` property has no visibility modifiers and is\n * therefore visible in all phases.\n */\nenum Lifecycle {\n  Create,\n  Read,\n  Update,\n}\n\n/**\n * A visibility filter, used to specify which properties should be included when\n * using the `withVisibilityFilter` decorator.\n *\n * The filter matches any property with ALL of the following:\n * - If the `any` key is present, the property must have at least one of the specified visibilities.\n * - If the `all` key is present, the property must have all of the specified visibilities.\n * - If the `none` key is present, the property must have none of the specified visibilities.\n */\nmodel VisibilityFilter {\n  any?: EnumMember[];\n  all?: EnumMember[];\n  none?: EnumMember[];\n}\n\n/**\n * Applies the given visibility filter to the properties of the target model.\n *\n * This transformation is recursive, so it will also apply the filter to any nested\n * or referenced models that are the types of any properties in the `target`.\n *\n * @param target The model to apply the visibility filter to.\n * @param filter The visibility filter to apply to the properties of the target model.\n *\n * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * @withVisibilityFilter(#{ all: #[Lifecycle.Read] })\n * model DogRead {\n *  ...Dog\n * }\n * ```\n */\nextern dec withVisibilityFilter(target: Model, filter: valueof VisibilityFilter);\n\n/**\n * Transforms the `target` model to include only properties that are visible during the\n * \"Update\" lifecycle phase.\n *\n * Any nested models of optional properties will be transformed into the \"CreateOrUpdate\"\n * lifecycle phase instead of the \"Update\" lifecycle phase, so that nested models may be\n * fully updated.\n *\n * @param target The model to apply the transformation to.\n *\n * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   @visibility(Lifecycle.Create, Lifecycle.Update)\n *   secretName: string;\n *\n *   name: string;\n * }\n *\n * @withLifecycleUpdate\n * model DogUpdate {\n *   ...Dog\n * }\n * ```\n */\nextern dec withLifecycleUpdate(target: Model);\n\n/**\n * A copy of the input model `T` with only the properties that are visible during the\n * \"Create\" resource lifecycle phase.\n *\n * This transformation is recursive, and will include only properties that have the\n * `Lifecycle.Create` visibility modifier.\n *\n * If a `NameTemplate` is provided, the new model will be named according to the template.\n * The template uses the same syntax as the `@friendlyName` decorator.\n *\n * @template T The model to transform.\n * @template NameTemplate The name template to use for the new model.\n *\n *  * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * model CreateDog is Create<Dog>;\n * ```\n */\n@friendlyName(NameTemplate, T)\n@withVisibilityFilter(#{ all: #[Lifecycle.Create] })\nmodel Create<T extends Reflection.Model, NameTemplate extends valueof string = \"Create{name}\"> {\n  ...T;\n}\n\n/**\n * A copy of the input model `T` with only the properties that are visible during the\n * \"Read\" resource lifecycle phase.\n *\n * This transformation is recursive, and will include only properties that have the\n * `Lifecycle.Read` visibility modifier.\n *\n * If a `NameTemplate` is provided, the new model will be named according to the template.\n * The template uses the same syntax as the `@friendlyName` decorator.\n *\n * @template T The model to transform.\n * @template NameTemplate The name template to use for the new model.\n *\n *  * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * model ReadDog is Read<Dog>;\n * ```\n */\n@friendlyName(NameTemplate, T)\n@withVisibilityFilter(#{ all: #[Lifecycle.Read] })\nmodel Read<T extends Reflection.Model, NameTemplate extends valueof string = \"Read{name}\"> {\n  ...T;\n}\n\n/**\n * A copy of the input model `T` with only the properties that are visible during the\n * \"Update\" resource lifecycle phase.\n *\n * This transformation will include only the properties that have the `Lifecycle.Update`\n * visibility modifier, and the types of all properties will be replaced with the\n * equivalent `CreateOrUpdate` transformation.\n *\n * If a `NameTemplate` is provided, the new model will be named according to the template.\n * The template uses the same syntax as the `@friendlyName` decorator.\n *\n * @template T The model to transform.\n * @template NameTemplate The name template to use for the new model.\n *\n *  * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * model UpdateDog is Update<Dog>;\n * ```\n */\n@friendlyName(NameTemplate, T)\n@withLifecycleUpdate\nmodel Update<T extends Reflection.Model, NameTemplate extends valueof string = \"Update{name}\"> {\n  ...T;\n}\n\n/**\n * A copy of the input model `T` with only the properties that are visible during the\n * \"Create\" or \"Update\" resource lifecycle phases.\n *\n * This transformation is recursive, and will include only properties that have the\n * `Lifecycle.Create` or `Lifecycle.Update` visibility modifier.\n *\n * If a `NameTemplate` is provided, the new model will be named according to the template.\n * The template uses the same syntax as the `@friendlyName` decorator.\n *\n * @template T The model to transform.\n * @template NameTemplate The name template to use for the new model.\n *\n *  * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * model CreateOrUpdateDog is CreateOrUpdate<Dog>;\n * ```\n */\n@friendlyName(NameTemplate, T)\n@withVisibilityFilter(#{ any: #[Lifecycle.Create, Lifecycle.Update] })\nmodel CreateOrUpdate<\n  T extends Reflection.Model,\n  NameTemplate extends valueof string = \"CreateOrUpdate{name}\"\n> {\n  ...T;\n}\n",
  "lib/aaz.tsp": "import \"../dist/src/index.js\";"
};
const _TypeSpecLibrary_ = {
  jsSourceFiles: TypeSpecJSSources,
  typespecSourceFiles: TypeSpecSources,
};

export { $lib, $onEmit, _TypeSpecLibrary_ };
