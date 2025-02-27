import { createTypeSpecLibrary, paramMessage, createDiagnosticCollector, getMinValue, getMaxValue, ignoreDiagnostics, isArrayModelType, reportDeprecated, validateDecoratorUniqueOnNode, typespecTypeToJson, getDoc, validateDecoratorTarget, SyntaxKind, getParameterVisibility, isVisible as isVisible$1, getEffectiveModelType, compilerAssert, walkPropertiesInherited, getProperty, getDiscriminator, filterModelProperties, navigateType, getEncode, createRule, defineLinter, isNullType, isErrorModel, isVoidType, getErrorsDoc, getReturnsDoc, listOperationsIn, listServices, navigateProgram, getOverloadedOperation, getOverloads, getVisibility, $visibility } from '@typespec/compiler';
import { TwoLevelMap, DuplicateTracker, deepClone, deepEquals } from '@typespec/compiler/utils';

const $lib = createTypeSpecLibrary({
    name: "@typespec/http",
    diagnostics: {
        "http-verb-duplicate": {
            severity: "error",
            messages: {
                default: paramMessage `HTTP verb already applied to ${"entityName"}`,
            },
        },
        "missing-uri-param": {
            severity: "error",
            messages: {
                default: paramMessage `Route reference parameter '${"param"}' but wasn't found in operation parameters`,
            },
        },
        "incompatible-uri-param": {
            severity: "error",
            messages: {
                default: paramMessage `Parameter '${"param"}' is defined in the uri as a ${"uriKind"} but is annotated as a ${"annotationKind"}.`,
            },
        },
        "use-uri-template": {
            severity: "error",
            messages: {
                default: paramMessage `Parameter '${"param"}' is already defined in the uri template. Explode, style and allowReserved property must be defined in the uri template as described by RFC 6570.`,
            },
        },
        "optional-path-param": {
            severity: "error",
            messages: {
                default: paramMessage `Path parameter '${"paramName"}' cannot be optional.`,
            },
        },
        "missing-server-param": {
            severity: "error",
            messages: {
                default: paramMessage `Server url contains parameter '${"param"}' but wasn't found in given parameters`,
            },
        },
        "duplicate-body": {
            severity: "error",
            messages: {
                default: "Operation has multiple @body parameters declared",
                duplicateUnannotated: "Operation has multiple unannotated parameters. There can only be one representing the body",
                bodyAndUnannotated: "Operation has a @body and an unannotated parameter. There can only be one representing the body",
            },
        },
        "duplicate-route-decorator": {
            severity: "error",
            messages: {
                namespace: "@route was defined twice on this namespace and has different values.",
            },
        },
        "operation-param-duplicate-type": {
            severity: "error",
            messages: {
                default: paramMessage `Param ${"paramName"} has multiple types: [${"types"}]`,
            },
        },
        "duplicate-operation": {
            severity: "error",
            messages: {
                default: paramMessage `Duplicate operation "${"operationName"}" routed at "${"verb"} ${"path"}".`,
            },
        },
        "multiple-status-codes": {
            severity: "error",
            messages: {
                default: "Multiple `@statusCode` decorators defined for this operation response.",
            },
        },
        "status-code-invalid": {
            severity: "error",
            messages: {
                default: "statusCode value must be a numeric or string literal or union of numeric or string literals",
                value: "statusCode value must be a three digit code between 100 and 599",
            },
        },
        "content-type-string": {
            severity: "error",
            messages: {
                default: "contentType parameter must be a string literal or union of string literals",
            },
        },
        "content-type-ignored": {
            severity: "warning",
            messages: {
                default: "`Content-Type` header ignored because there is no body.",
            },
        },
        "metadata-ignored": {
            severity: "warning",
            messages: {
                default: paramMessage `${"kind"} property will be ignored as it is inside of a @body property. Use @bodyRoot instead if wanting to mix.`,
            },
        },
        "response-cookie-not-supported": {
            severity: "warning",
            messages: {
                default: paramMessage `@cookie on response is not supported. Property '${"propName"}' will be ignored in the body. If you need 'Set-Cookie', use @header instead.`,
            },
        },
        "no-service-found": {
            severity: "warning",
            messages: {
                default: paramMessage `No namespace with '@service' was found, but Namespace '${"namespace"}' contains routes. Did you mean to annotate this with '@service'?`,
            },
        },
        "invalid-type-for-auth": {
            severity: "error",
            messages: {
                default: paramMessage `@useAuth ${"kind"} only accept Auth model, Tuple of auth model or union of auth model.`,
            },
        },
        "shared-inconsistency": {
            severity: "error",
            messages: {
                default: paramMessage `Each operation routed at "${"verb"} ${"path"}" needs to have the @sharedRoute decorator.`,
            },
        },
        "write-visibility-not-supported": {
            severity: "warning",
            messages: {
                default: `@visibility("write") is not supported. Use @visibility("update"), @visibility("create") or @visibility("create", "update") as appropriate.`,
            },
        },
        "multipart-invalid-content-type": {
            severity: "error",
            messages: {
                default: paramMessage `Content type '${"contentType"}' is not a multipart content type. Supported content types are: ${"supportedContentTypes"}.`,
            },
        },
        "multipart-model": {
            severity: "error",
            messages: {
                default: "Multipart request body must be a model.",
            },
        },
        "multipart-part": {
            severity: "error",
            messages: {
                default: "Expect item to be an HttpPart model.",
            },
        },
        "multipart-nested": {
            severity: "error",
            messages: {
                default: "Cannot use @multipartBody inside of an HttpPart",
            },
        },
        "http-file-extra-property": {
            severity: "error",
            messages: {
                default: paramMessage `File model cannot define extra properties. Found '${"propName"}'.`,
            },
        },
        "formdata-no-part-name": {
            severity: "error",
            messages: {
                default: "Part used in multipart/form-data must have a name.",
            },
        },
        "header-format-required": {
            severity: "error",
            messages: {
                default: `A format must be specified for @header when type is an array. e.g. @header({format: "csv"})`,
            },
        },
    },
    state: {
        authentication: { description: "State for the @auth decorator" },
        header: { description: "State for the @header decorator" },
        cookie: { description: "State for the @cookie decorator" },
        query: { description: "State for the @query decorator" },
        path: { description: "State for the @path decorator" },
        body: { description: "State for the @body decorator" },
        bodyRoot: { description: "State for the @bodyRoot decorator" },
        bodyIgnore: { description: "State for the @bodyIgnore decorator" },
        multipartBody: { description: "State for the @bodyIgnore decorator" },
        statusCode: { description: "State for the @statusCode decorator" },
        verbs: { description: "State for the verb decorators (@get, @post, @put, etc.)" },
        servers: { description: "State for the @server decorator" },
        includeInapplicableMetadataInPayload: {
            description: "State for the @includeInapplicableMetadataInPayload decorator",
        },
        // route.ts
        externalInterfaces: {},
        routeProducer: {},
        routes: {},
        sharedRoutes: { description: "State for the @sharedRoute decorator" },
        routeOptions: {},
        // private
        file: { description: "State for the @Private.file decorator" },
        httpPart: { description: "State for the @Private.httpPart decorator" },
    },
});
const { reportDiagnostic, createDiagnostic, stateKeys: HttpStateKeys } = $lib;

function error(target) {
    return [
        [],
        [
            createDiagnostic({
                code: "status-code-invalid",
                target,
                messageId: "value",
            }),
        ],
    ];
}
// Issue a diagnostic if not valid
function validateStatusCode(code, diagnosticTarget) {
    const codeAsNumber = typeof code === "string" ? parseInt(code, 10) : code;
    if (isNaN(codeAsNumber)) {
        return error(diagnosticTarget);
    }
    if (!Number.isInteger(codeAsNumber)) {
        return error(diagnosticTarget);
    }
    if (codeAsNumber < 100 || codeAsNumber > 599) {
        return error(diagnosticTarget);
    }
    return [[codeAsNumber], []];
}
function getStatusCodesFromType(program, type, diagnosticTarget) {
    switch (type.kind) {
        case "String":
        case "Number":
            return validateStatusCode(type.value, diagnosticTarget);
        case "Union":
            const diagnostics = createDiagnosticCollector();
            const statusCodes = [...type.variants.values()].flatMap((variant) => {
                return diagnostics.pipe(getStatusCodesFromType(program, variant.type, diagnosticTarget));
            });
            return diagnostics.wrap(statusCodes);
        case "Scalar":
            return validateStatusCodeRange(program, type, type, diagnosticTarget);
        case "ModelProperty":
            if (type.type.kind === "Scalar") {
                return validateStatusCodeRange(program, type, type.type, diagnosticTarget);
            }
            else {
                return getStatusCodesFromType(program, type.type, diagnosticTarget);
            }
        default:
            return error(diagnosticTarget);
    }
}
function validateStatusCodeRange(program, type, scalar, diagnosticTarget) {
    if (!isInt32(program, scalar)) {
        return error(diagnosticTarget);
    }
    const range = getStatusCodesRange(program, type);
    if (isRangeComplete(range)) {
        return [[range], []];
    }
    else {
        return error(diagnosticTarget); // TODO better error explaining missing start/end
    }
}
function isRangeComplete(range) {
    return range.start !== undefined && range.end !== undefined;
}
function getStatusCodesRange(program, type, diagnosticTarget) {
    const start = getMinValue(program, type);
    const end = getMaxValue(program, type);
    let baseRange = {};
    if (type.kind === "ModelProperty" &&
        (type.type.kind === "Scalar" || type.type.kind === "ModelProperty")) {
        baseRange = getStatusCodesRange(program, type.type);
    }
    else if (type.kind === "Scalar" && type.baseScalar) {
        baseRange = getStatusCodesRange(program, type.baseScalar);
    }
    return { ...baseRange, start, end };
}
function isInt32(program, type) {
    return ignoreDiagnostics(program.checker.isTypeAssignableTo(type.projectionBase ?? type, program.checker.getStdType("int32"), type));
}

/**
 * Extract params to be interpolated(Wrapped in '{' and '}'}) from a path/url.
 * @param path Path/Url
 *
 * @example "foo/{name}/bar" -> ["name"]
 */
function extractParamsFromPath(path) {
    return path.match(/\{[^}]+\}/g)?.map((s) => s.slice(1, -1)) ?? [];
}

const namespace$1 = "TypeSpec.Http";
const $header = (context, entity, headerNameOrOptions) => {
    const options = {
        type: "header",
        name: entity.name.replace(/([a-z])([A-Z])/g, "$1-$2").toLowerCase(),
    };
    if (headerNameOrOptions) {
        if (headerNameOrOptions.kind === "String") {
            options.name = headerNameOrOptions.value;
        }
        else if (headerNameOrOptions.kind === "Model") {
            const name = headerNameOrOptions.properties.get("name")?.type;
            if (name?.kind === "String") {
                options.name = name.value;
            }
            const format = headerNameOrOptions.properties.get("format")?.type;
            if (format?.kind === "String") {
                const val = format.value;
                if (val === "csv" ||
                    val === "tsv" ||
                    val === "pipes" ||
                    val === "ssv" ||
                    val === "simple" ||
                    val === "form" ||
                    val === "multi") {
                    options.format = val;
                }
            }
        }
        else {
            return;
        }
    }
    if (entity.type.kind === "Model" &&
        isArrayModelType(context.program, entity.type) &&
        options.format === undefined) {
        reportDiagnostic(context.program, {
            code: "header-format-required",
            target: context.decoratorTarget,
        });
    }
    context.program.stateMap(HttpStateKeys.header).set(entity, options);
};
function getHeaderFieldOptions(program, entity) {
    return program.stateMap(HttpStateKeys.header).get(entity);
}
function getHeaderFieldName(program, entity) {
    return getHeaderFieldOptions(program, entity)?.name;
}
function isHeader(program, entity) {
    return program.stateMap(HttpStateKeys.header).has(entity);
}
/** {@inheritDoc CookieDecorator } */
const $cookie = (context, entity, cookieNameOrOptions) => {
    const paramName = typeof cookieNameOrOptions === "string"
        ? cookieNameOrOptions
        : (cookieNameOrOptions?.name ??
            entity.name.replace(/([a-z])([A-Z])/g, "$1_$2").toLowerCase());
    const options = {
        type: "cookie",
        name: paramName,
    };
    context.program.stateMap(HttpStateKeys.cookie).set(entity, options);
};
/**
 * Get the cookie parameter options for the given entity.
 * @param program
 * @param entity
 * @returns The cookie parameter options or undefined if the entity is not a cookie parameter.
 */
function getCookieParamOptions(program, entity) {
    return program.stateMap(HttpStateKeys.cookie).get(entity);
}
/**
 * Check whether the given entity is a cookie parameter.
 * @param program
 * @param entity
 * @returns True if the entity is a cookie parameter, false otherwise.
 */
function isCookieParam(program, entity) {
    return program.stateMap(HttpStateKeys.cookie).has(entity);
}
const $query = (context, entity, queryNameOrOptions) => {
    const paramName = typeof queryNameOrOptions === "string"
        ? queryNameOrOptions
        : (queryNameOrOptions?.name ?? entity.name);
    const userOptions = typeof queryNameOrOptions === "object" ? queryNameOrOptions : {};
    if (userOptions.format) {
        reportDeprecated(context.program, "The `format` option of `@query` decorator is deprecated. Use `explode: true` instead of `form` and `multi`. `csv` or `simple` is the default now.", entity);
    }
    const options = {
        type: "query",
        explode: userOptions.explode ?? (userOptions.format === "multi" || userOptions.format === "form"),
        format: userOptions.format,
        name: paramName,
    };
    if (entity.type.kind === "Model" &&
        isArrayModelType(context.program, entity.type) &&
        // eslint-disable-next-line @typescript-eslint/no-deprecated
        options.format === undefined) {
        // eslint-disable-next-line @typescript-eslint/no-deprecated
        options.format = userOptions.explode ? "multi" : "csv";
    }
    context.program.stateMap(HttpStateKeys.query).set(entity, options);
};
function getQueryParamOptions(program, entity) {
    return program.stateMap(HttpStateKeys.query).get(entity);
}
function getQueryParamName(program, entity) {
    return getQueryParamOptions(program, entity)?.name;
}
function isQueryParam(program, entity) {
    return program.stateMap(HttpStateKeys.query).has(entity);
}
const $path = (context, entity, paramNameOrOptions) => {
    const paramName = typeof paramNameOrOptions === "string"
        ? paramNameOrOptions
        : (paramNameOrOptions?.name ?? entity.name);
    const userOptions = typeof paramNameOrOptions === "object" ? paramNameOrOptions : {};
    const options = {
        type: "path",
        explode: userOptions.explode ?? false,
        allowReserved: userOptions.allowReserved ?? false,
        style: userOptions.style ?? "simple",
        name: paramName,
    };
    context.program.stateMap(HttpStateKeys.path).set(entity, options);
};
function getPathParamOptions(program, entity) {
    return program.stateMap(HttpStateKeys.path).get(entity);
}
function getPathParamName(program, entity) {
    return getPathParamOptions(program, entity)?.name;
}
function isPathParam(program, entity) {
    return program.stateMap(HttpStateKeys.path).has(entity);
}
const $body = (context, entity) => {
    context.program.stateSet(HttpStateKeys.body).add(entity);
};
const $bodyRoot = (context, entity) => {
    context.program.stateSet(HttpStateKeys.bodyRoot).add(entity);
};
const $bodyIgnore = (context, entity) => {
    context.program.stateSet(HttpStateKeys.bodyIgnore).add(entity);
};
function isBody(program, entity) {
    return program.stateSet(HttpStateKeys.body).has(entity);
}
function isBodyRoot(program, entity) {
    return program.stateSet(HttpStateKeys.bodyRoot).has(entity);
}
function isBodyIgnore(program, entity) {
    return program.stateSet(HttpStateKeys.bodyIgnore).has(entity);
}
const $multipartBody = (context, entity) => {
    context.program.stateSet(HttpStateKeys.multipartBody).add(entity);
};
function isMultipartBodyProperty(program, entity) {
    return program.stateSet(HttpStateKeys.multipartBody).has(entity);
}
const $statusCode = (context, entity) => {
    context.program.stateSet(HttpStateKeys.statusCode).add(entity);
    // eslint-disable-next-line @typescript-eslint/no-deprecated
    setLegacyStatusCodeState(context, entity);
};
/**
 * To not break we keep the legacy behavior of resolving the discrete status code in the decorator and saving them in the state.
 * @deprecated To remove. Added in October 2023 sprint.
 */
function setLegacyStatusCodeState(context, entity) {
    const codes = [];
    if (entity.type.kind === "String") {
        if (validStatusCode(context.program, entity.type.value, entity)) {
            codes.push(entity.type.value);
        }
    }
    else if (entity.type.kind === "Number") {
        if (validStatusCode(context.program, String(entity.type.value), entity)) {
            codes.push(String(entity.type.value));
        }
    }
    else if (entity.type.kind === "Union") {
        for (const variant of entity.type.variants.values()) {
            const option = variant.type;
            if (option.kind === "String") {
                if (validStatusCode(context.program, option.value, option)) {
                    codes.push(option.value);
                }
            }
            else if (option.kind === "Number") {
                if (validStatusCode(context.program, String(option.value), option)) {
                    codes.push(String(option.value));
                }
            }
        }
    }
    // Check status code value: 3 digits with first digit in [1-5]
    // Issue a diagnostic if not valid
    function validStatusCode(program, code, entity) {
        const statusCodePattern = /[1-5][0-9][0-9]/;
        if (code.match(statusCodePattern)) {
            return true;
        }
        reportDiagnostic(program, {
            code: "status-code-invalid",
            target: entity,
            messageId: "value",
        });
        return false;
    }
    context.program.stateMap(HttpStateKeys.statusCode).set(entity, codes);
}
/**
 * @deprecated DO NOT USE, for internal use only.
 */
function setStatusCode(program, entity, codes) {
    program.stateMap(HttpStateKeys.statusCode).set(entity, codes);
}
function isStatusCode(program, entity) {
    return program.stateMap(HttpStateKeys.statusCode).has(entity);
}
function getStatusCodesWithDiagnostics(program, type) {
    return getStatusCodesFromType(program, type, type);
}
function getStatusCodes(program, entity) {
    return ignoreDiagnostics(getStatusCodesWithDiagnostics(program, entity));
}
// Reference: https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
function getStatusCodeDescription(statusCode) {
    if (typeof statusCode === "object") {
        return rangeDescription(statusCode.start, statusCode.end);
    }
    const statusCodeNumber = typeof statusCode === "string" ? parseInt(statusCode, 10) : statusCode;
    switch (statusCodeNumber) {
        case 200:
            return "The request has succeeded.";
        case 201:
            return "The request has succeeded and a new resource has been created as a result.";
        case 202:
            return "The request has been accepted for processing, but processing has not yet completed.";
        case 204:
            return "There is no content to send for this request, but the headers may be useful. ";
        case 301:
            return "The URL of the requested resource has been changed permanently. The new URL is given in the response.";
        case 304:
            return "The client has made a conditional request and the resource has not been modified.";
        case 400:
            return "The server could not understand the request due to invalid syntax.";
        case 401:
            return "Access is unauthorized.";
        case 403:
            return "Access is forbidden.";
        case 404:
            return "The server cannot find the requested resource.";
        case 409:
            return "The request conflicts with the current state of the server.";
        case 412:
            return "Precondition failed.";
        case 503:
            return "Service unavailable.";
    }
    return rangeDescription(statusCodeNumber, statusCodeNumber);
}
function rangeDescription(start, end) {
    if (start >= 100 && end <= 199) {
        return "Informational";
    }
    else if (start >= 200 && end <= 299) {
        return "Successful";
    }
    else if (start >= 300 && end <= 399) {
        return "Redirection";
    }
    else if (start >= 400 && end <= 499) {
        return "Client error";
    }
    else if (start >= 500 && end <= 599) {
        return "Server error";
    }
    return undefined;
}
function setOperationVerb(context, entity, verb) {
    validateVerbUniqueOnNode(context, entity);
    context.program.stateMap(HttpStateKeys.verbs).set(entity, verb);
}
function validateVerbUniqueOnNode(context, type) {
    const verbDecorators = type.decorators.filter((x) => VERB_DECORATORS.includes(x.decorator) &&
        x.node?.kind === SyntaxKind.DecoratorExpression &&
        x.node?.parent === type.node);
    if (verbDecorators.length > 1) {
        reportDiagnostic(context.program, {
            code: "http-verb-duplicate",
            format: { entityName: type.name },
            target: context.decoratorTarget,
        });
        return false;
    }
    return true;
}
function getOperationVerb(program, entity) {
    return program.stateMap(HttpStateKeys.verbs).get(entity);
}
function createVerbDecorator(verb) {
    return (context, entity) => {
        setOperationVerb(context, entity, verb);
    };
}
const $get = createVerbDecorator("get");
const $put = createVerbDecorator("put");
const $post = createVerbDecorator("post");
const $patch = createVerbDecorator("patch");
const $delete = createVerbDecorator("delete");
const $head = createVerbDecorator("head");
const VERB_DECORATORS = [$get, $head, $post, $put, $patch, $delete];
/**
 * Configure the server url for the service.
 * @param context Decorator context
 * @param target Decorator target (must be a namespace)
 * @param description Description for this server.
 * @param parameters @optional Parameters to interpolate in the server url.
 */
const $server = (context, target, url, description, parameters) => {
    const params = extractParamsFromPath(url);
    const parameterMap = new Map(parameters?.properties ?? []);
    for (const declaredParam of params) {
        const param = parameterMap.get(declaredParam);
        if (!param) {
            reportDiagnostic(context.program, {
                code: "missing-server-param",
                format: { param: declaredParam },
                target: context.getArgumentTarget(0),
            });
            parameterMap.delete(declaredParam);
        }
    }
    let servers = context.program.stateMap(HttpStateKeys.servers).get(target);
    if (servers === undefined) {
        servers = [];
        context.program.stateMap(HttpStateKeys.servers).set(target, servers);
    }
    servers.push({ url, description, parameters: parameterMap });
};
function getServers(program, type) {
    return program.stateMap(HttpStateKeys.servers).get(type);
}
function $useAuth(context, entity, authConfig) {
    validateDecoratorUniqueOnNode(context, entity, $useAuth);
    const [auth, diagnostics] = extractAuthentication(context.program, authConfig);
    if (diagnostics.length > 0)
        context.program.reportDiagnostics(diagnostics);
    if (auth !== undefined) {
        setAuthentication(context.program, entity, auth);
    }
}
function setAuthentication(program, entity, auth) {
    program.stateMap(HttpStateKeys.authentication).set(entity, auth);
}
function extractAuthentication(program, type) {
    const diagnostics = createDiagnosticCollector();
    switch (type.kind) {
        case "Model":
            const auth = diagnostics.pipe(extractHttpAuthentication(program, type, type));
            if (auth === undefined)
                return diagnostics.wrap(undefined);
            return diagnostics.wrap({ options: [{ schemes: [auth] }] });
        case "Tuple":
            const option = diagnostics.pipe(extractHttpAuthenticationOption(program, type, type));
            return diagnostics.wrap({ options: [option] });
        case "Union":
            return extractHttpAuthenticationOptions(program, type, type);
        default:
            return [
                undefined,
                [
                    createDiagnostic({
                        code: "invalid-type-for-auth",
                        format: { kind: type.kind },
                        target: type,
                    }),
                ],
            ];
    }
}
function extractHttpAuthenticationOptions(program, tuple, diagnosticTarget) {
    const options = [];
    const diagnostics = createDiagnosticCollector();
    for (const variant of tuple.variants.values()) {
        const value = variant.type;
        switch (value.kind) {
            case "Model":
                const result = diagnostics.pipe(extractHttpAuthentication(program, value, diagnosticTarget));
                if (result !== undefined) {
                    options.push({ schemes: [result] });
                }
                break;
            case "Tuple":
                const option = diagnostics.pipe(extractHttpAuthenticationOption(program, value, diagnosticTarget));
                options.push(option);
                break;
            default:
                diagnostics.add(createDiagnostic({
                    code: "invalid-type-for-auth",
                    format: { kind: value.kind },
                    target: value,
                }));
        }
    }
    return diagnostics.wrap({ options });
}
function extractHttpAuthenticationOption(program, tuple, diagnosticTarget) {
    const schemes = [];
    const diagnostics = createDiagnosticCollector();
    for (const value of tuple.values) {
        switch (value.kind) {
            case "Model":
                const result = diagnostics.pipe(extractHttpAuthentication(program, value, diagnosticTarget));
                if (result !== undefined) {
                    schemes.push(result);
                }
                break;
            default:
                diagnostics.add(createDiagnostic({
                    code: "invalid-type-for-auth",
                    format: { kind: value.kind },
                    target: value,
                }));
        }
    }
    return diagnostics.wrap({ schemes });
}
function extractHttpAuthentication(program, modelType, diagnosticTarget) {
    const [result, diagnostics] = typespecTypeToJson(modelType, diagnosticTarget);
    if (result === undefined) {
        return [result, diagnostics];
    }
    const description = getDoc(program, modelType);
    const auth = result.type === "oauth2"
        ? extractOAuth2Auth(modelType, result)
        : { ...result, model: modelType };
    return [
        {
            ...auth,
            id: modelType.name || result.type,
            ...(description && { description }),
        },
        diagnostics,
    ];
}
function extractOAuth2Auth(modelType, data) {
    // Validation of OAuth2Flow models in this function is minimal because the
    // type system already validates whether the model represents a flow
    // configuration.  This code merely avoids runtime errors.
    const flows = Array.isArray(data.flows) && data.flows.every((x) => typeof x === "object")
        ? data.flows
        : [];
    const defaultScopes = Array.isArray(data.defaultScopes) ? data.defaultScopes : [];
    return {
        id: data.id,
        type: data.type,
        model: modelType,
        flows: flows.map((flow) => {
            const scopes = flow.scopes ? flow.scopes : defaultScopes;
            return {
                ...flow,
                scopes: scopes.map((x) => ({ value: x })),
            };
        }),
    };
}
function getAuthentication(program, entity) {
    return program.stateMap(HttpStateKeys.authentication).get(entity);
}
/**
 * `@route` defines the relative route URI for the target operation
 *
 * The first argument should be a URI fragment that may contain one or more path parameter fields.
 * If the namespace or interface that contains the operation is also marked with a `@route` decorator,
 * it will be used as a prefix to the route URI of the operation.
 *
 * `@route` can only be applied to operations, namespaces, and interfaces.
 */
const $route = (context, entity, path, parameters) => {
    validateDecoratorUniqueOnNode(context, entity, $route);
    // Handle the deprecated `shared` option
    let shared = false;
    const sharedValue = parameters?.properties.get("shared")?.type;
    if (sharedValue !== undefined) {
        reportDeprecated(context.program, "The `shared` option is deprecated, use the `@sharedRoute` decorator instead.", entity);
        // The type checker should have raised a diagnostic if the value isn't boolean
        if (sharedValue.kind === "Boolean") {
            shared = sharedValue.value;
        }
    }
    setRoute(context, entity, {
        path,
        shared,
    });
};
/**
 * `@sharedRoute` marks the operation as sharing a route path with other operations.
 *
 * When an operation is marked with `@sharedRoute`, it enables other operations to share the same
 * route path as long as those operations are also marked with `@sharedRoute`.
 *
 * `@sharedRoute` can only be applied directly to operations.
 */
const $sharedRoute = (context, entity) => {
    setSharedRoute(context.program, entity);
};
/**
 * Specifies if inapplicable metadata should be included in the payload for
 * the given entity. This is true by default unless changed by this
 * decorator.
 *
 * @param entity Target model, namespace, or model property. If applied to a
 *               model or namespace, applies recursively to child models,
 *               namespaces, and model properties unless overridden by
 *               applying this decorator to a child.
 *
 * @param value `true` to include inapplicable metadata in payload, false to
 *               exclude it.
 *
 * @see isApplicableMetadata
 *
 * @ignore Cause issue with conflicting function of same name for now
 */
function $includeInapplicableMetadataInPayload(context, entity, value) {
    if (!validateDecoratorTarget(context, entity, "@includeInapplicableMetadataInPayload", [
        "Namespace",
        "Model",
        "ModelProperty",
    ])) {
        return;
    }
    const state = context.program.stateMap(HttpStateKeys.includeInapplicableMetadataInPayload);
    state.set(entity, value);
}
/**
 * Determines if the given model property should be included in the payload if it is
 * inapplicable metadata.
 *
 * @see isApplicableMetadata
 * @see $includeInapplicableMetadataInPayload
 */
function includeInapplicableMetadataInPayload(program, property) {
    let e;
    for (e = property; e; e = e.kind === "ModelProperty" ? e.model : e.namespace) {
        const value = program.stateMap(HttpStateKeys.includeInapplicableMetadataInPayload).get(e);
        if (value !== undefined) {
            return value;
        }
    }
    return true;
}

/**
 * Flags enum representation of well-known visibilities that are used in
 * REST API.
 */
var Visibility;
(function (Visibility) {
    Visibility[Visibility["Read"] = 1] = "Read";
    Visibility[Visibility["Create"] = 2] = "Create";
    Visibility[Visibility["Update"] = 4] = "Update";
    Visibility[Visibility["Delete"] = 8] = "Delete";
    Visibility[Visibility["Query"] = 16] = "Query";
    Visibility[Visibility["None"] = 0] = "None";
    Visibility[Visibility["All"] = 31] = "All";
    /**
     * Additional flag to indicate when something is nested in a collection
     * and therefore no metadata is applicable.
     */
    Visibility[Visibility["Item"] = 1048576] = "Item";
    /**
     * Additional flag to indicate when the verb is path and therefore
     * will have fields made optional if request visibility includes update.
     */
    Visibility[Visibility["Patch"] = 2097152] = "Patch";
})(Visibility || (Visibility = {}));
const visibilityToArrayMap = new Map();
function visibilityToArray(visibility) {
    // Item and Patch flags are not real visibilities.
    visibility &= ~Visibility.Item;
    visibility &= ~Visibility.Patch;
    let result = visibilityToArrayMap.get(visibility);
    if (!result) {
        result = [];
        if (visibility & Visibility.Read) {
            result.push("read");
        }
        if (visibility & Visibility.Create) {
            result.push("create");
        }
        if (visibility & Visibility.Update) {
            result.push("update");
        }
        if (visibility & Visibility.Delete) {
            result.push("delete");
        }
        if (visibility & Visibility.Query) {
            result.push("query");
        }
        compilerAssert(result.length > 0 || visibility === Visibility.None, "invalid visibility");
        visibilityToArrayMap.set(visibility, result);
    }
    return result;
}
function arrayToVisibility(array) {
    if (!array) {
        return undefined;
    }
    let value = Visibility.None;
    for (const item of array) {
        switch (item) {
            case "read":
                value |= Visibility.Read;
                break;
            case "create":
                value |= Visibility.Create;
                break;
            case "update":
                value |= Visibility.Update;
                break;
            case "delete":
                value |= Visibility.Delete;
                break;
            case "query":
                value |= Visibility.Query;
                break;
            default:
                return undefined;
        }
    }
    return value;
}
/**
 * Provides a naming suffix to create a unique name for a type with this
 * visibility.
 *
 * The canonical visibility (default Visibility.Read) gets empty suffix,
 * otherwise visibilities are joined in pascal-case with `Or`. And `Item` is
 * if `Visibility.Item` is produced.
 *
 * Examples (with canonicalVisibility = Visibility.Read):
 *  - Visibility.Read => ""
 *  - Visibility.Update => "Update"
 *  - Visibility.Create | Visibility.Update => "CreateOrUpdate"
 *  - Visibility.Create | Visibility.Item => "CreateItem"
 *  - Visibility.Create | Visibility.Update | Visibility.Item => "CreateOrUpdateItem"
 *  */
function getVisibilitySuffix(visibility, canonicalVisibility = Visibility.None) {
    let suffix = "";
    if ((visibility & ~Visibility.Item & ~Visibility.Patch) !== canonicalVisibility) {
        const visibilities = visibilityToArray(visibility);
        suffix += visibilities.map((v) => v[0].toUpperCase() + v.slice(1)).join("Or");
    }
    if (visibility & Visibility.Item) {
        suffix += "Item";
    }
    return suffix;
}
/**
 * Determines the visibility to use for a request with the given verb.
 *
 * - GET | HEAD => Visibility.Query
 * - POST => Visibility.Update
 * - PUT => Visibility.Create | Update
 * - DELETE => Visibility.Delete
 */
function getDefaultVisibilityForVerb(verb) {
    switch (verb) {
        case "get":
        case "head":
            return Visibility.Query;
        case "post":
            return Visibility.Create;
        case "put":
            return Visibility.Create | Visibility.Update;
        case "patch":
            return Visibility.Update;
        case "delete":
            return Visibility.Delete;
        default:
            compilerAssert(false, "unreachable");
    }
}
/**
 * Determines the visibility to use for a request with the given verb.
 *
 * - GET | HEAD => Visibility.Query
 * - POST => Visibility.Create
 * - PATCH => Visibility.Update
 * - PUT => Visibility.Create | Update
 * - DELETE => Visibility.Delete
 * @param verb The HTTP verb for the operation.
 * @deprecated Use `resolveRequestVisibility` instead, or if you only want the default visibility for a verb, `getDefaultVisibilityForVerb`.
 * @returns The applicable parameter visibility or visibilities for the request.
 */
function getRequestVisibility(verb) {
    let visibility = getDefaultVisibilityForVerb(verb);
    // If the verb is PATCH, then we need to add the patch flag to the visibility in order for
    // later processes to properly apply it
    if (verb === "patch") {
        visibility |= Visibility.Patch;
    }
    return visibility;
}
/**
 * Returns the applicable parameter visibility or visibilities for the request if `@requestVisibility` was used.
 * Otherwise, returns the default visibility based on the HTTP verb for the operation.
 * @param operation The TypeSpec Operation for the request.
 * @param verb The HTTP verb for the operation.
 * @returns The applicable parameter visibility or visibilities for the request.
 */
function resolveRequestVisibility(program, operation, verb) {
    const parameterVisibility = getParameterVisibility(program, operation);
    const parameterVisibilityArray = arrayToVisibility(parameterVisibility);
    const defaultVisibility = getDefaultVisibilityForVerb(verb);
    let visibility = parameterVisibilityArray ?? defaultVisibility;
    // If the verb is PATCH, then we need to add the patch flag to the visibility in order for
    // later processes to properly apply it
    if (verb === "patch") {
        visibility |= Visibility.Patch;
    }
    return visibility;
}
/**
 * Determines if a property is metadata. A property is defined to be
 * metadata if it is marked `@header`, `@cookie`, `@query`, `@path`, or `@statusCode`.
 */
function isMetadata(program, property) {
    return (isHeader(program, property) ||
        isCookieParam(program, property) ||
        isQueryParam(program, property) ||
        isPathParam(program, property) ||
        isStatusCode(program, property));
}
/**
 * Determines if the given property is visible with the given visibility.
 */
function isVisible(program, property, visibility) {
    // eslint-disable-next-line @typescript-eslint/no-deprecated
    return isVisible$1(program, property, visibilityToArray(visibility));
}
/**
 * Determines if the given property is metadata that is applicable with the
 * given visibility.
 *
 * - No metadata is applicable with Visibility.Item present.
 * - If only Visibility.Read is present, then only `@header` and `@status`
 *   properties are applicable.
 * - If Visibility.Read is not present, all metadata properties other than
 *   `@statusCode` are applicable.
 */
function isApplicableMetadata(program, property, visibility, isMetadataCallback = isMetadata) {
    return isApplicableMetadataCore(program, property, visibility, false, isMetadataCallback);
}
/**
 * Determines if the given property is metadata or marked `@body` and
 * applicable with the given visibility.
 */
function isApplicableMetadataOrBody(program, property, visibility, isMetadataCallback = isMetadata) {
    return isApplicableMetadataCore(program, property, visibility, true, isMetadataCallback);
}
function isApplicableMetadataCore(program, property, visibility, treatBodyAsMetadata, isMetadataCallback) {
    if (visibility & Visibility.Item) {
        return false; // no metadata is applicable to collection items
    }
    if (treatBodyAsMetadata &&
        (isBody(program, property) ||
            isBodyRoot(program, property) ||
            isMultipartBodyProperty(program, property))) {
        return true;
    }
    if (!isMetadataCallback(program, property)) {
        return false;
    }
    if (visibility & Visibility.Read) {
        return isHeader(program, property) || isStatusCode(program, property);
    }
    if (!(visibility & Visibility.Read)) {
        return !isStatusCode(program, property);
    }
    return true;
}
function createMetadataInfo(program, options) {
    const canonicalVisibility = options?.canonicalVisibility ?? Visibility.None;
    const stateMap = new TwoLevelMap();
    return {
        isEmptied,
        isTransformed,
        isPayloadProperty,
        isOptional,
        getEffectivePayloadType,
    };
    function isEmptied(type, visibility) {
        if (!type) {
            return false;
        }
        const state = getState(type, visibility);
        return state === 2 /* State.Emptied */;
    }
    function isTransformed(type, visibility) {
        if (!type) {
            return false;
        }
        const state = getState(type, visibility);
        switch (state) {
            case 1 /* State.Transformed */:
                return true;
            case 2 /* State.Emptied */:
                return visibility === canonicalVisibility || !isEmptied(type, canonicalVisibility);
            default:
                return false;
        }
    }
    function getState(type, visibility) {
        return stateMap.getOrAdd(type, visibility, () => computeState(type, visibility), 3 /* State.ComputationInProgress */);
    }
    function computeState(type, visibility) {
        switch (type.kind) {
            case "Model":
                return computeStateForModel(type, visibility);
            case "Union":
                return computeStateForUnion(type, visibility);
            default:
                return 0 /* State.NotTransformed */;
        }
    }
    function computeStateForModel(model, visibility) {
        if (computeIsEmptied(model, visibility)) {
            return 2 /* State.Emptied */;
        }
        if (isTransformed(model.indexer?.value, visibility | Visibility.Item) ||
            isTransformed(model.baseModel, visibility)) {
            return 1 /* State.Transformed */;
        }
        for (const property of model.properties.values()) {
            if (isAddedRemovedOrMadeOptional(property, visibility) ||
                isTransformed(property.type, visibility)) {
                return 1 /* State.Transformed */;
            }
        }
        return 0 /* State.NotTransformed */;
    }
    function computeStateForUnion(union, visibility) {
        for (const variant of union.variants.values()) {
            if (isTransformed(variant.type, visibility)) {
                return 1 /* State.Transformed */;
            }
        }
        return 0 /* State.NotTransformed */;
    }
    function isAddedRemovedOrMadeOptional(property, visibility) {
        if (visibility === canonicalVisibility) {
            return false;
        }
        if (isOptional(property, canonicalVisibility) !== isOptional(property, visibility)) {
            return true;
        }
        return (isPayloadProperty(property, visibility, undefined, /* keep shared */ true) !==
            isPayloadProperty(property, canonicalVisibility, undefined, /*keep shared*/ true));
    }
    function computeIsEmptied(model, visibility) {
        if (model.baseModel || model.indexer || model.properties.size === 0) {
            return false;
        }
        for (const property of model.properties.values()) {
            if (isPayloadProperty(property, visibility, undefined, /* keep shared */ true)) {
                return false;
            }
        }
        return true;
    }
    function isOptional(property, visibility) {
        // Properties are made optional for patch requests if the visibility includes
        // update, but not for array elements with the item flag since you must provide
        // all array elements with required properties, even in a patch.
        const hasUpdate = (visibility & Visibility.Update) !== 0;
        const isPatch = (visibility & Visibility.Patch) !== 0;
        const isItem = (visibility & Visibility.Item) !== 0;
        return property.optional || (hasUpdate && isPatch && !isItem);
    }
    function isPayloadProperty(property, visibility, inExplicitBody, keepShareableProperties) {
        if (!inExplicitBody &&
            (isBodyIgnore(program, property) ||
                isApplicableMetadata(program, property, visibility) ||
                (isMetadata(program, property) && !includeInapplicableMetadataInPayload(program, property)))) {
            return false;
        }
        if (!isVisible(program, property, visibility)) {
            // NOTE: When we check if a model is transformed for a given
            // visibility, we retain shared properties. It is not considered
            // transformed if the only removed properties are shareable. However,
            // if we do create a unique schema for a visibility, then we still
            // drop invisible shareable properties from other uses of
            // isPayloadProperty.
            //
            // For OpenAPI emit, for example, this means that we won't put a
            // readOnly: true property into a specialized schema for a non-read
            // visibility.
            keepShareableProperties ??= visibility === canonicalVisibility;
            return !!(keepShareableProperties && options?.canShareProperty?.(property));
        }
        return true;
    }
    /**
     * If the type is an anonymous model, tries to find a named model that has the same
     * set of properties when non-payload properties are excluded.we
     */
    function getEffectivePayloadType(type, visibility) {
        if (type.kind === "Model" && !type.name) {
            const effective = getEffectiveModelType(program, type, (p) => isPayloadProperty(p, visibility, undefined, /* keep shared */ false));
            if (effective.name) {
                return effective;
            }
        }
        return type;
    }
}

/**
 * @deprecated Use `OperationProperty.kind === 'contentType'` instead.
 * Check if the given model property is the content type header.
 * @param program Program
 * @param property Model property.
 * @returns True if the model property is marked as a header and has the name `content-type`(case insensitive.)
 */
function isContentTypeHeader(program, property) {
    const headerName = getHeaderFieldName(program, property);
    return Boolean(headerName && headerName.toLowerCase() === "content-type");
}
/**
 * Resolve the content types from a model property by looking at the value.
 * @property property Model property
 * @returns List of contnet types and any diagnostics if there was an issue.
 */
function getContentTypes(property) {
    const diagnostics = createDiagnosticCollector();
    if (property.type.kind === "String") {
        return [[property.type.value], []];
    }
    else if (property.type.kind === "Union") {
        const contentTypes = [];
        for (const option of property.type.variants.values()) {
            if (option.type.kind === "String") {
                contentTypes.push(option.type.value);
            }
            else {
                diagnostics.add(createDiagnostic({
                    code: "content-type-string",
                    target: property,
                }));
                continue;
            }
        }
        return diagnostics.wrap(contentTypes);
    }
    else if (property.type.kind === "Scalar" && property.type.name === "string") {
        return [["*/*"], []];
    }
    return [[], [createDiagnostic({ code: "content-type-string", target: property })]];
}

/**
 * Find the type of a property in a model
 */
function getHttpProperty(program, property, path, options = {}) {
    const diagnostics = [];
    function createResult(opts) {
        return [{ ...opts, property, path }, diagnostics];
    }
    const annotations = {
        header: getHeaderFieldOptions(program, property),
        cookie: getCookieParamOptions(program, property),
        query: getQueryParamOptions(program, property),
        path: getPathParamOptions(program, property),
        body: isBody(program, property),
        bodyRoot: isBodyRoot(program, property),
        multipartBody: isMultipartBodyProperty(program, property),
        statusCode: isStatusCode(program, property),
    };
    const defined = Object.entries(annotations).filter((x) => !!x[1]);
    const implicit = options.implicitParameter?.(property);
    if (implicit && defined.length > 0) {
        if (implicit.type === "path" && annotations.path) {
            if (annotations.path.explode ||
                annotations.path.style !== "simple" ||
                annotations.path.allowReserved) {
                diagnostics.push(createDiagnostic({
                    code: "use-uri-template",
                    format: {
                        param: property.name,
                    },
                    target: property,
                }));
            }
        }
        else if (implicit.type === "query" && annotations.query) {
            if (annotations.query.explode) {
                diagnostics.push(createDiagnostic({
                    code: "use-uri-template",
                    format: {
                        param: property.name,
                    },
                    target: property,
                }));
            }
        }
        else {
            diagnostics.push(createDiagnostic({
                code: "incompatible-uri-param",
                format: {
                    param: property.name,
                    uriKind: implicit.type,
                    annotationKind: defined[0][0],
                },
                target: property,
            }));
        }
    }
    // if implicit just returns as it is. Validation above would have checked nothing was set explicitly apart from the type and that the type match
    if (implicit) {
        return createResult({
            kind: implicit.type,
            options: implicit,
            property,
        });
    }
    if (defined.length === 0) {
        return createResult({ kind: "bodyProperty" });
    }
    else if (defined.length > 1) {
        diagnostics.push(createDiagnostic({
            code: "operation-param-duplicate-type",
            format: { paramName: property.name, types: defined.map((x) => x[0]).join(", ") },
            target: property,
        }));
    }
    if (annotations.header) {
        if (annotations.header.name.toLowerCase() === "content-type") {
            return createResult({ kind: "contentType" });
        }
        else {
            return createResult({ kind: "header", options: annotations.header });
        }
    }
    else if (annotations.cookie) {
        return createResult({ kind: "cookie", options: annotations.cookie });
    }
    else if (annotations.query) {
        return createResult({ kind: "query", options: annotations.query });
    }
    else if (annotations.path) {
        return createResult({ kind: "path", options: annotations.path });
    }
    else if (annotations.statusCode) {
        return createResult({ kind: "statusCode" });
    }
    else if (annotations.body) {
        return createResult({ kind: "body" });
    }
    else if (annotations.bodyRoot) {
        return createResult({ kind: "bodyRoot" });
    }
    else if (annotations.multipartBody) {
        return createResult({ kind: "multipartBody" });
    }
    compilerAssert(false, `Unexpected http property type`);
}
/**
 * Walks the given input(request parameters or response) and return all the properties and where they should be included(header, query, path, body, as a body property, etc.)
 *
 * @param rootMapOut If provided, the map will be populated to link nested metadata properties to their root properties.
 */
function resolvePayloadProperties(program, type, visibility, options = {}) {
    const diagnostics = createDiagnosticCollector();
    const httpProperties = new Map();
    if (type.kind !== "Model" || type.properties.size === 0) {
        return diagnostics.wrap([]);
    }
    const visited = new Set();
    function checkModel(model, path) {
        visited.add(model);
        let foundBody = false;
        let foundBodyProperty = false;
        for (const property of walkPropertiesInherited(model)) {
            const propPath = [...path, property.name];
            if (!isVisible(program, property, visibility)) {
                continue;
            }
            let httpProperty = diagnostics.pipe(getHttpProperty(program, property, propPath, options));
            if (shouldTreatAsBodyProperty(httpProperty, visibility)) {
                httpProperty = { kind: "bodyProperty", property, path: propPath };
            }
            // Ignore cookies in response to avoid future breaking changes to @cookie.
            // https://github.com/microsoft/typespec/pull/4761#discussion_r1805082132
            if (httpProperty.kind === "cookie" && visibility & Visibility.Read) {
                diagnostics.add(createDiagnostic({
                    code: "response-cookie-not-supported",
                    target: property,
                    format: { propName: property.name },
                }));
                continue;
            }
            if (httpProperty.kind === "body" ||
                httpProperty.kind === "bodyRoot" ||
                httpProperty.kind === "multipartBody") {
                foundBody = true;
            }
            if (!(httpProperty.kind === "body" || httpProperty.kind === "multipartBody") &&
                isModelWithProperties(property.type) &&
                !visited.has(property.type)) {
                if (checkModel(property.type, propPath)) {
                    foundBody = true;
                    continue;
                }
            }
            if (httpProperty.kind === "bodyProperty") {
                foundBodyProperty = true;
            }
            httpProperties.set(property, httpProperty);
        }
        return foundBody && !foundBodyProperty;
    }
    checkModel(type, []);
    return diagnostics.wrap([...httpProperties.values()]);
}
function isModelWithProperties(type) {
    return type.kind === "Model" && !type.indexer && type.properties.size > 0;
}
function shouldTreatAsBodyProperty(property, visibility) {
    if (visibility & Visibility.Read) {
        return property.kind === "query" || property.kind === "path";
    }
    if (!(visibility & Visibility.Read)) {
        return property.kind === "statusCode";
    }
    return false;
}

/** @internal */
const namespace = "TypeSpec.Http.Private";
const $plainData = (context, entity) => {
    const { program } = context;
    const decoratorsToRemove = ["$header", "$body", "$query", "$path", "$statusCode"];
    const [headers, bodies, queries, paths, statusCodes] = [
        program.stateMap(HttpStateKeys.header),
        program.stateSet(HttpStateKeys.body),
        program.stateMap(HttpStateKeys.query),
        program.stateMap(HttpStateKeys.path),
        program.stateMap(HttpStateKeys.statusCode),
    ];
    for (const property of entity.properties.values()) {
        // Remove the decorators so that they do not run in the future, for example,
        // if this model is later spread into another.
        property.decorators = property.decorators.filter((d) => !decoratorsToRemove.includes(d.decorator.name));
        // Remove the impact the decorators already had on this model.
        headers.delete(property);
        bodies.delete(property);
        queries.delete(property);
        paths.delete(property);
        statusCodes.delete(property);
    }
};
const $httpFile = (context, target) => {
    context.program.stateSet(HttpStateKeys.file).add(target);
};
/**
 * Check if the given type is an `HttpFile`
 */
function isHttpFile(program, type) {
    return program.stateSet(HttpStateKeys.file).has(type);
}
function isOrExtendsHttpFile(program, type) {
    if (type.kind !== "Model") {
        return false;
    }
    let current = type;
    while (current) {
        if (isHttpFile(program, current)) {
            return true;
        }
        current = current.baseModel;
    }
    return false;
}
function getHttpFileModel(program, type) {
    if (type.kind !== "Model" || !isOrExtendsHttpFile(program, type)) {
        return undefined;
    }
    const contentType = getProperty(type, "contentType");
    const filename = getProperty(type, "filename");
    const contents = getProperty(type, "contents");
    return { contents, contentType, filename, type };
}
const $httpPart = (context, target, type, options) => {
    context.program.stateMap(HttpStateKeys.httpPart).set(target, { type, options });
};
/** Return the http part information on a model that is an `HttpPart` */
function getHttpPart(program, target) {
    return program.stateMap(HttpStateKeys.httpPart).get(target);
}
/** @internal */
const $decorators$1 = {
    "TypeSpec.Http.Private": {
        httpFile: $httpFile,
        httpPart: $httpPart,
        plainData: $plainData,
    },
};

var f2 = /*#__PURE__*/Object.freeze({
    __proto__: null,
    $decorators: $decorators$1,
    getHttpFileModel: getHttpFileModel,
    getHttpPart: getHttpPart,
    isHttpFile: isHttpFile,
    isOrExtendsHttpFile: isOrExtendsHttpFile,
    namespace: namespace
});

function resolveHttpPayload(program, type, visibility, usedIn, options = {}) {
    const diagnostics = createDiagnosticCollector();
    const metadata = diagnostics.pipe(resolvePayloadProperties(program, type, visibility, options));
    const body = diagnostics.pipe(resolveBody(program, type, metadata, visibility, usedIn));
    if (body) {
        if (body.contentTypes.includes("multipart/form-data") &&
            body.bodyKind === "single" &&
            body.type.kind !== "Model") {
            diagnostics.add(createDiagnostic({
                code: "multipart-model",
                target: body.property ?? type,
            }));
            return diagnostics.wrap({ body: undefined, metadata });
        }
    }
    return diagnostics.wrap({ body, metadata });
}
function resolveBody(program, requestOrResponseType, metadata, visibility, usedIn) {
    const diagnostics = createDiagnosticCollector();
    const resolvedContentTypes = diagnostics.pipe(resolveContentTypes(program, metadata, usedIn));
    const file = getHttpFileModel(program, requestOrResponseType);
    if (file !== undefined) {
        const file = getHttpFileModel(program, requestOrResponseType);
        return diagnostics.wrap({
            bodyKind: "single",
            contentTypes: diagnostics.pipe(getContentTypes(file.contentType)),
            contentTypeProperty: file.contentType,
            type: file.contents.type,
            isExplicit: false,
            containsMetadataAnnotations: false,
        });
    }
    // non-model or intrinsic/array model -> response body is response type
    if (requestOrResponseType.kind !== "Model" || isArrayModelType(program, requestOrResponseType)) {
        return diagnostics.wrap({
            bodyKind: "single",
            ...resolvedContentTypes,
            type: requestOrResponseType,
            isExplicit: false,
            containsMetadataAnnotations: false,
        });
    }
    // look for explicit body
    const resolvedBody = diagnostics.pipe(resolveExplicitBodyProperty(program, metadata, resolvedContentTypes, visibility, usedIn));
    if (resolvedBody === undefined) {
        // Special case if the model as a parent model then we'll return an empty object as this is assumed to be a nominal type.
        // Special Case if the model has an indexer then it means it can return props so cannot be void.
        if (requestOrResponseType.baseModel || requestOrResponseType.indexer) {
            return diagnostics.wrap({
                bodyKind: "single",
                ...resolvedContentTypes,
                type: requestOrResponseType,
                isExplicit: false,
                containsMetadataAnnotations: false,
            });
        }
        // Special case for legacy purposes if the return type is an empty model with only @discriminator("xyz")
        // Then we still want to return that object as it technically always has a body with that implicit property.
        if (requestOrResponseType.derivedModels.length > 0 &&
            getDiscriminator(program, requestOrResponseType)) {
            return diagnostics.wrap({
                bodyKind: "single",
                ...resolvedContentTypes,
                type: requestOrResponseType,
                isExplicit: false,
                containsMetadataAnnotations: false,
            });
        }
    }
    const unannotatedProperties = filterModelProperties(program, requestOrResponseType, (p) => metadata.some((x) => x.property === p && x.kind === "bodyProperty"));
    if (unannotatedProperties.properties.size > 0) {
        if (resolvedBody === undefined) {
            return diagnostics.wrap({
                bodyKind: "single",
                ...resolvedContentTypes,
                type: unannotatedProperties,
                isExplicit: false,
                containsMetadataAnnotations: false,
            });
        }
        else {
            diagnostics.add(createDiagnostic({
                code: "duplicate-body",
                messageId: "bodyAndUnannotated",
                target: requestOrResponseType,
            }));
        }
    }
    if (resolvedBody === undefined && resolvedContentTypes.contentTypeProperty) {
        diagnostics.add(createDiagnostic({
            code: "content-type-ignored",
            target: resolvedContentTypes.contentTypeProperty,
        }));
    }
    return diagnostics.wrap(resolvedBody);
}
function resolveContentTypes(program, metadata, usedIn) {
    for (const prop of metadata) {
        if (prop.kind === "contentType") {
            const [contentTypes, diagnostics] = getContentTypes(prop.property);
            return [{ contentTypes, contentTypeProperty: prop.property }, diagnostics];
        }
    }
    switch (usedIn) {
        case "multipart":
            // Figure this out later
            return [{ contentTypes: [] }, []];
        default:
            return [{ contentTypes: ["application/json"] }, []];
    }
}
function resolveExplicitBodyProperty(program, metadata, resolvedContentTypes, visibility, usedIn) {
    const diagnostics = createDiagnosticCollector();
    let resolvedBody;
    const duplicateTracker = new DuplicateTracker();
    for (const item of metadata) {
        if (item.kind === "body" || item.kind === "bodyRoot" || item.kind === "multipartBody") {
            duplicateTracker.track("body", item.property);
        }
        switch (item.kind) {
            case "body":
            case "bodyRoot":
                let containsMetadataAnnotations = false;
                if (item.kind === "body") {
                    const valid = diagnostics.pipe(validateBodyProperty(program, item.property, usedIn));
                    containsMetadataAnnotations = !valid;
                }
                if (resolvedBody === undefined) {
                    resolvedBody = {
                        bodyKind: "single",
                        ...resolvedContentTypes,
                        type: item.property.type,
                        isExplicit: item.kind === "body",
                        containsMetadataAnnotations,
                        property: item.property,
                        parameter: item.property,
                    };
                }
                break;
            case "multipartBody":
                resolvedBody = diagnostics.pipe(resolveMultiPartBody(program, item.property, resolvedContentTypes, visibility));
                break;
        }
    }
    for (const [_, items] of duplicateTracker.entries()) {
        for (const prop of items) {
            diagnostics.add(createDiagnostic({
                code: "duplicate-body",
                target: prop,
            }));
        }
    }
    return diagnostics.wrap(resolvedBody);
}
/** Validate a property marked with `@body` */
function validateBodyProperty(program, property, usedIn) {
    const diagnostics = createDiagnosticCollector();
    navigateType(property.type, {
        modelProperty: (prop) => {
            const kind = isHeader(program, prop)
                ? "header"
                : // also emit metadata-ignored for response cookie
                    (usedIn === "request" || usedIn === "response") && isCookieParam(program, prop)
                        ? "cookie"
                        : (usedIn === "request" || usedIn === "multipart") && isQueryParam(program, prop)
                            ? "query"
                            : usedIn === "request" && isPathParam(program, prop)
                                ? "path"
                                : usedIn === "response" && isStatusCode(program, prop)
                                    ? "statusCode"
                                    : undefined;
            if (kind) {
                diagnostics.add(createDiagnostic({
                    code: "metadata-ignored",
                    format: { kind },
                    target: prop,
                }));
            }
        },
    }, {});
    return diagnostics.wrap(diagnostics.diagnostics.length === 0);
}
function resolveMultiPartBody(program, property, resolvedContentTypes, visibility) {
    const type = property.type;
    if (type.kind === "Model") {
        return resolveMultiPartBodyFromModel(program, property, type, resolvedContentTypes, visibility);
    }
    else if (type.kind === "Tuple") {
        return resolveMultiPartBodyFromTuple(program, property, type, resolvedContentTypes, visibility);
    }
    else {
        return [undefined, [createDiagnostic({ code: "multipart-model", target: property })]];
    }
}
function resolveMultiPartBodyFromModel(program, property, type, resolvedContentTypes, visibility) {
    const diagnostics = createDiagnosticCollector();
    const parts = [];
    for (const item of type.properties.values()) {
        const part = diagnostics.pipe(resolvePartOrParts(program, item.type, visibility));
        if (part) {
            parts.push({ ...part, name: part.name ?? item.name, optional: item.optional });
        }
    }
    return diagnostics.wrap({
        bodyKind: "multipart",
        ...resolvedContentTypes,
        parts,
        property,
        type,
    });
}
const multipartContentTypes = {
    formData: "multipart/form-data",
    mixed: "multipart/mixed",
};
const multipartContentTypesValues = Object.values(multipartContentTypes);
function resolveMultiPartBodyFromTuple(program, property, type, resolvedContentTypes, visibility) {
    const diagnostics = createDiagnosticCollector();
    const parts = [];
    for (const contentType of resolvedContentTypes.contentTypes) {
        if (!multipartContentTypesValues.includes(contentType)) {
            diagnostics.add(createDiagnostic({
                code: "multipart-invalid-content-type",
                format: { contentType, supportedContentTypes: multipartContentTypesValues.join(", ") },
                target: type,
            }));
        }
    }
    for (const [index, item] of type.values.entries()) {
        const part = diagnostics.pipe(resolvePartOrParts(program, item, visibility));
        if (part?.name === undefined &&
            resolvedContentTypes.contentTypes.includes(multipartContentTypes.formData)) {
            diagnostics.add(createDiagnostic({
                code: "formdata-no-part-name",
                target: type.node.values[index],
            }));
        }
        if (part) {
            parts.push(part);
        }
    }
    return diagnostics.wrap({
        bodyKind: "multipart",
        ...resolvedContentTypes,
        parts,
        property,
        type,
    });
}
function resolvePartOrParts(program, type, visibility) {
    if (type.kind === "Model" && isArrayModelType(program, type)) {
        const [part, diagnostics] = resolvePart(program, type.indexer.value, visibility);
        if (part) {
            return [{ ...part, multi: true }, diagnostics];
        }
        return [part, diagnostics];
    }
    else {
        return resolvePart(program, type, visibility);
    }
}
function resolvePart(program, type, visibility) {
    const part = getHttpPart(program, type);
    if (part) {
        const file = getHttpFileModel(program, part.type);
        if (file !== undefined) {
            return getFilePart(part.options.name, file);
        }
        let [{ body, metadata }, diagnostics] = resolveHttpPayload(program, part.type, visibility, "multipart");
        if (body === undefined) {
            return [undefined, diagnostics];
        }
        else if (body.bodyKind === "multipart") {
            return [undefined, [createDiagnostic({ code: "multipart-nested", target: type })]];
        }
        if (body.contentTypes.length === 0) {
            body = { ...body, contentTypes: resolveDefaultContentTypeForPart(program, body.type) };
        }
        return [
            {
                multi: false,
                name: part.options.name,
                body,
                optional: false,
                headers: metadata.filter((x) => x.kind === "header"),
            },
            diagnostics,
        ];
    }
    return [undefined, [createDiagnostic({ code: "multipart-part", target: type })]];
}
function getFilePart(name, file) {
    const [contentTypes, diagnostics] = getContentTypes(file.contentType);
    return [
        {
            multi: false,
            name,
            body: {
                bodyKind: "single",
                contentTypeProperty: file.contentType,
                contentTypes: contentTypes,
                type: file.contents.type,
                isExplicit: false,
                containsMetadataAnnotations: false,
            },
            filename: file.filename,
            optional: false,
            headers: [],
        },
        diagnostics,
    ];
}
function resolveDefaultContentTypeForPart(program, type) {
    function resolve(type) {
        if (type.kind === "Scalar") {
            const encodedAs = getEncode(program, type);
            if (encodedAs) {
                type = encodedAs.type;
            }
            if (ignoreDiagnostics(program.checker.isTypeAssignableTo(type.projectionBase ?? type, program.checker.getStdType("bytes"), type))) {
                return ["application/octet-stream"];
            }
            else {
                return ["text/plain"];
            }
        }
        else if (type.kind === "Union") {
            return [...type.variants.values()].flatMap((x) => resolve(x.type));
        }
        else {
            return ["application/json"];
        }
    }
    return [...new Set(resolve(type))];
}

const operators = ["+", "#", ".", "/", ";", "?", "&"];
const uriTemplateRegex = /\{([^{}]+)\}|([^{}]+)/g;
const expressionRegex = /([^:*]*)(?::(\d+)|(\*))?/;
/**
 * Parse a URI template according to [RFC-6570](https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.3)
 */
function parseUriTemplate(template) {
    const parameters = [];
    const segments = [];
    const matches = template.matchAll(uriTemplateRegex);
    for (let [_, expression, literal] of matches) {
        if (expression) {
            let operator;
            if (operators.includes(expression[0])) {
                operator = expression[0];
                expression = expression.slice(1);
            }
            const items = expression.split(",");
            for (const item of items) {
                const match = item.match(expressionRegex);
                const name = match[1];
                const parameter = {
                    name: name,
                    operator,
                    modifier: match[3]
                        ? { type: "explode" }
                        : match[2]
                            ? { type: "prefix", value: Number(match[2]) }
                            : undefined,
                };
                parameters.push(parameter);
                segments.push(parameter);
            }
        }
        else {
            segments.push(literal);
        }
    }
    return { segments, parameters };
}

function getOperationParameters(program, operation, partialUriTemplate, overloadBase, options = {}) {
    const verb = (options?.verbSelector && options.verbSelector(program, operation)) ??
        getOperationVerb(program, operation) ??
        overloadBase?.verb;
    if (verb) {
        return getOperationParametersForVerb(program, operation, verb, partialUriTemplate);
    }
    // If no verb is explicitly specified, it is POST if there is a body and
    // GET otherwise. Theoretically, it is possible to use @visibility
    // strangely such that there is no body if the verb is POST and there is a
    // body if the verb is GET. In that rare case, GET is chosen arbitrarily.
    const post = getOperationParametersForVerb(program, operation, "post", partialUriTemplate);
    return post[0].body
        ? post
        : getOperationParametersForVerb(program, operation, "get", partialUriTemplate);
}
const operatorToStyle = {
    ";": "matrix",
    "#": "fragment",
    ".": "label",
    "/": "path",
};
function getOperationParametersForVerb(program, operation, verb, partialUriTemplate) {
    const diagnostics = createDiagnosticCollector();
    const visibility = resolveRequestVisibility(program, operation, verb);
    const parsedUriTemplate = parseUriTemplate(partialUriTemplate);
    const parameters = [];
    const { body: resolvedBody, metadata } = diagnostics.pipe(resolveHttpPayload(program, operation.parameters, visibility, "request", {
        implicitParameter: (param) => {
            const isTopLevel = param.model === operation.parameters;
            const uriParam = isTopLevel && parsedUriTemplate.parameters.find((x) => x.name === param.name);
            if (!uriParam) {
                return undefined;
            }
            const explode = uriParam.modifier?.type === "explode";
            if (uriParam.operator === "?" || uriParam.operator === "&") {
                return {
                    type: "query",
                    name: uriParam.name,
                    explode,
                };
            }
            else if (uriParam.operator === "+") {
                return {
                    type: "path",
                    name: uriParam.name,
                    explode,
                    allowReserved: true,
                    style: "simple",
                };
            }
            else {
                return {
                    type: "path",
                    name: uriParam.name,
                    explode,
                    allowReserved: false,
                    style: (uriParam.operator && operatorToStyle[uriParam.operator]) ?? "simple",
                };
            }
        },
    }));
    for (const item of metadata) {
        switch (item.kind) {
            case "contentType":
                parameters.push({
                    name: "Content-Type",
                    type: "header",
                    param: item.property,
                });
                break;
            case "path":
                if (item.property.optional) {
                    diagnostics.add(createDiagnostic({
                        code: "optional-path-param",
                        format: { paramName: item.property.name },
                        target: item.property,
                    }));
                }
            // eslint-disable-next-line no-fallthrough
            case "query":
            case "cookie":
            case "header":
                parameters.push({
                    ...item.options,
                    param: item.property,
                });
                break;
        }
    }
    const body = resolvedBody;
    return diagnostics.wrap({
        properties: metadata,
        parameters,
        verb,
        body,
        get bodyType() {
            return body?.type;
        },
        get bodyParameter() {
            return body?.property;
        },
    });
}

// The set of allowed segment separator characters
const AllowedSegmentSeparators = ["/", ":"];
function normalizeFragment(fragment, trimLast = false) {
    if (fragment.length > 0 && AllowedSegmentSeparators.indexOf(fragment[0]) < 0) {
        // Insert the default separator
        fragment = `/${fragment}`;
    }
    if (trimLast && fragment[fragment.length - 1] === "/") {
        return fragment.slice(0, -1);
    }
    return fragment;
}
function joinPathSegments(rest) {
    let current = "";
    for (const [index, segment] of rest.entries()) {
        current += normalizeFragment(segment, index < rest.length - 1);
    }
    return current;
}
function buildPath(pathFragments) {
    // Join all fragments with leading and trailing slashes trimmed
    const path = pathFragments.length === 0 ? "/" : joinPathSegments(pathFragments);
    // The final path must start with a '/'
    return path[0] === "/" ? path : `/${path}`;
}
function resolvePathAndParameters(program, operation, overloadBase, options) {
    const diagnostics = createDiagnosticCollector();
    const { uriTemplate, parameters } = diagnostics.pipe(getUriTemplateAndParameters(program, operation, overloadBase, options));
    const parsedUriTemplate = parseUriTemplate(uriTemplate);
    // Pull out path parameters to verify what's in the path string
    const paramByName = new Set(parameters.parameters
        .filter(({ type }) => type === "path" || type === "query")
        .map((x) => x.name));
    // Ensure that all of the parameters defined in the route are accounted for in
    // the operation parameters
    for (const routeParam of parsedUriTemplate.parameters) {
        const decoded = decodeURIComponent(routeParam.name);
        if (!paramByName.has(routeParam.name) && !paramByName.has(decoded)) {
            diagnostics.add(createDiagnostic({
                code: "missing-uri-param",
                format: { param: routeParam.name },
                target: operation,
            }));
        }
    }
    const path = produceLegacyPathFromUriTemplate(parsedUriTemplate);
    return diagnostics.wrap({
        uriTemplate,
        path,
        parameters,
    });
}
function produceLegacyPathFromUriTemplate(uriTemplate) {
    let result = "";
    for (const segment of uriTemplate.segments ?? []) {
        if (typeof segment === "string") {
            result += segment;
        }
        else if (segment.operator !== "?" && segment.operator !== "&") {
            result += `{${segment.name}}`;
        }
    }
    return result;
}
function collectSegmentsAndOptions(program, source) {
    if (source === undefined)
        return [[], {}];
    const [parentSegments, parentOptions] = collectSegmentsAndOptions(program, source.namespace);
    const route = getRoutePath(program, source)?.path;
    const options = source.kind === "Namespace" ? (getRouteOptionsForNamespace(program, source) ?? {}) : {};
    return [[...parentSegments, ...(route ? [route] : [])], { ...parentOptions, ...options }];
}
function getUriTemplateAndParameters(program, operation, overloadBase, options) {
    const [parentSegments, parentOptions] = collectSegmentsAndOptions(program, operation.interface ?? operation.namespace);
    const routeProducer = getRouteProducer(program, operation) ?? DefaultRouteProducer;
    const [result, diagnostics] = routeProducer(program, operation, parentSegments, overloadBase, {
        ...parentOptions,
        ...options,
    });
    return [
        { uriTemplate: buildPath([result.uriTemplate]), parameters: result.parameters },
        diagnostics,
    ];
}
/**
 * @deprecated DO NOT USE. For internal use only as a workaround.
 * @param program Program
 * @param target Target namespace
 * @param sourceInterface Interface that should be included in namespace.
 */
function includeInterfaceRoutesInNamespace(program, target, sourceInterface) {
    let array = program.stateMap(HttpStateKeys.externalInterfaces).get(target);
    if (array === undefined) {
        array = [];
        program.stateMap(HttpStateKeys.externalInterfaces).set(target, array);
    }
    array.push(sourceInterface);
}
function DefaultRouteProducer(program, operation, parentSegments, overloadBase, options) {
    const diagnostics = createDiagnosticCollector();
    const routePath = getRoutePath(program, operation)?.path;
    const uriTemplate = !routePath && overloadBase
        ? overloadBase.uriTemplate
        : joinPathSegments([...parentSegments, ...(routePath ? [routePath] : [])]);
    const parsedUriTemplate = parseUriTemplate(uriTemplate);
    const parameters = diagnostics.pipe(getOperationParameters(program, operation, uriTemplate, overloadBase, options.paramOptions));
    // Pull out path parameters to verify what's in the path string
    const unreferencedPathParamNames = new Map(parameters.parameters
        .filter(({ type }) => type === "path" || type === "query")
        .map((x) => [x.name, x]));
    // Compile the list of all route params that aren't represented in the route
    for (const uriParam of parsedUriTemplate.parameters) {
        unreferencedPathParamNames.delete(uriParam.name);
    }
    const resolvedUriTemplate = addOperationTemplateToUriTemplate(uriTemplate, [
        ...unreferencedPathParamNames.values(),
    ]);
    return diagnostics.wrap({
        uriTemplate: resolvedUriTemplate,
        parameters,
    });
}
const styleToOperator = {
    matrix: ";",
    label: ".",
    simple: "",
    path: "/",
    fragment: "#",
};
function getUriTemplatePathParam(param) {
    const operator = param.allowReserved ? "+" : styleToOperator[param.style];
    return `{${operator}${param.name}${param.explode ? "*" : ""}}`;
}
function getUriTemplateQueryParamPart(param) {
    return `${escapeUriTemplateParamName(param.name)}${param.explode ? "*" : ""}`;
}
function addQueryParamsToUriTemplate(uriTemplate, params) {
    const queryParams = params.filter((x) => x.type === "query");
    return (uriTemplate +
        (queryParams.length > 0
            ? `{?${queryParams.map((x) => getUriTemplateQueryParamPart(x)).join(",")}}`
            : ""));
}
function addOperationTemplateToUriTemplate(uriTemplate, params) {
    const pathParams = params.filter((x) => x.type === "path").map(getUriTemplatePathParam);
    const queryParams = params.filter((x) => x.type === "query");
    const pathPart = joinPathSegments([uriTemplate, ...pathParams]);
    return addQueryParamsToUriTemplate(pathPart, queryParams);
}
function escapeUriTemplateParamName(name) {
    return name.replaceAll(":", "%3A");
}
function setRouteProducer(program, operation, routeProducer) {
    program.stateMap(HttpStateKeys.routeProducer).set(operation, routeProducer);
}
function getRouteProducer(program, operation) {
    return program.stateMap(HttpStateKeys.routeProducer).get(operation);
}
function setRoute(context, entity, details) {
    if (!validateDecoratorTarget(context, entity, "@route", ["Namespace", "Interface", "Operation"])) {
        return;
    }
    const state = context.program.stateMap(HttpStateKeys.routes);
    if (state.has(entity) && entity.kind === "Namespace") {
        const existingPath = state.get(entity);
        if (existingPath !== details.path) {
            reportDiagnostic(context.program, {
                code: "duplicate-route-decorator",
                messageId: "namespace",
                target: entity,
            });
        }
    }
    else {
        state.set(entity, details.path);
        if (entity.kind === "Operation" && details.shared) {
            setSharedRoute(context.program, entity);
        }
    }
}
function setSharedRoute(program, operation) {
    program.stateMap(HttpStateKeys.sharedRoutes).set(operation, true);
}
function isSharedRoute(program, operation) {
    return program.stateMap(HttpStateKeys.sharedRoutes).get(operation) === true;
}
function getRoutePath(program, entity) {
    const path = program.stateMap(HttpStateKeys.routes).get(entity);
    return path
        ? {
            path,
            shared: entity.kind === "Operation" && isSharedRoute(program, entity),
        }
        : undefined;
}
function setRouteOptionsForNamespace(program, namespace, options) {
    program.stateMap(HttpStateKeys.routeOptions).set(namespace, options);
}
function getRouteOptionsForNamespace(program, namespace) {
    return program.stateMap(HttpStateKeys.routeOptions).get(namespace);
}

const opReferenceContainerRouteRule = createRule({
    name: "op-reference-container-route",
    severity: "warning",
    description: "Check for referenced (`op is`) operations which have a @route on one of their containers.",
    url: "https://typespec.io/docs/libraries/http/rules/op-reference-container-route",
    messages: {
        default: paramMessage `Operation ${"opName"} references an operation which has a @route prefix on its namespace or interface: "${"routePrefix"}".  This operation will not carry forward the route prefix so the final route may be different than the referenced operation.`,
    },
    create(context) {
        // This algorithm traces operation references for each operation encountered
        // in the program.  It will locate the first referenced operation which has a
        // `@route` prefix on a parent namespace or interface.
        const checkedOps = new Map();
        function getContainerRoutePrefix(container) {
            if (container === undefined) {
                return undefined;
            }
            if (container.kind === "Operation") {
                return (getContainerRoutePrefix(container.interface) ??
                    getContainerRoutePrefix(container.namespace));
            }
            const route = getRoutePath(context.program, container);
            return route ? route.path : getContainerRoutePrefix(container.namespace);
        }
        function checkOperationReferences(op, originalOp) {
            if (op !== undefined) {
                // Skip this reference if the original operation shares the same
                // container with the referenced operation
                const container = op.interface ?? op.namespace;
                const originalContainer = originalOp.interface ?? originalOp.namespace;
                if (container !== originalContainer) {
                    let route = checkedOps.get(op);
                    if (route === undefined) {
                        route = getContainerRoutePrefix(op);
                        checkedOps.set(op, route);
                    }
                    if (route) {
                        context.reportDiagnostic({
                            target: originalOp,
                            format: { opName: originalOp.name, routePrefix: route },
                        });
                        return;
                    }
                }
                // Continue checking if the referenced operation didn't have a route prefix
                checkOperationReferences(op.sourceOperation, originalOp);
            }
        }
        return {
            operation: (op) => {
                checkOperationReferences(op.sourceOperation, op);
            },
        };
    },
});

const $linter = defineLinter({
    rules: [opReferenceContainerRouteRule],
});

/**
 * Resolve the authentication for a given operation.
 * @param program Program
 * @param operation Operation
 * @returns Authentication provided on the operation or containing interface or namespace.
 */
function getAuthenticationForOperation(program, operation) {
    const operationAuth = getAuthentication(program, operation);
    if (operationAuth) {
        return operationAuth;
    }
    if (operation.interface !== undefined) {
        const interfaceAuth = getAuthentication(program, operation.interface);
        if (interfaceAuth) {
            return interfaceAuth;
        }
    }
    let namespace = operation.namespace;
    while (namespace) {
        const namespaceAuth = getAuthentication(program, namespace);
        if (namespaceAuth) {
            return namespaceAuth;
        }
        namespace = namespace.namespace;
    }
    return undefined;
}
/**
 * Compute the authentication for a given service.
 * @param service Http Service
 * @returns The normalized authentication for a service.
 */
function resolveAuthentication(service) {
    let schemes = {};
    let defaultAuth = { options: [] };
    const operationsAuth = new Map();
    if (service.authentication) {
        const { newServiceSchemes, authOptions } = gatherAuth(service.authentication, {});
        schemes = newServiceSchemes;
        defaultAuth = authOptions;
    }
    for (const op of service.operations) {
        if (op.authentication) {
            const { newServiceSchemes, authOptions } = gatherAuth(op.authentication, schemes);
            schemes = newServiceSchemes;
            operationsAuth.set(op.operation, authOptions);
        }
    }
    return { schemes: Object.values(schemes), defaultAuth, operationsAuth };
}
function gatherAuth(authentication, serviceSchemes) {
    const newServiceSchemes = serviceSchemes;
    const authOptions = { options: [] };
    for (const option of authentication.options) {
        const authOption = { all: [] };
        for (const optionScheme of option.schemes) {
            const serviceScheme = serviceSchemes[optionScheme.id];
            let newServiceScheme = optionScheme;
            if (serviceScheme) {
                // If we've seen a different scheme by this id,
                // Make sure to not overwrite it
                if (!authsAreEqual(serviceScheme, optionScheme)) {
                    while (serviceSchemes[newServiceScheme.id]) {
                        newServiceScheme.id = newServiceScheme.id + "_";
                    }
                }
                // Merging scopes when encountering the same Oauth2 scheme
                else if (serviceScheme.type === "oauth2" && optionScheme.type === "oauth2") {
                    const x = mergeOAuthScopes(serviceScheme, optionScheme);
                    newServiceScheme = x;
                }
            }
            const httpAuthRef = makeHttpAuthRef(optionScheme, newServiceScheme);
            newServiceSchemes[newServiceScheme.id] = newServiceScheme;
            authOption.all.push(httpAuthRef);
        }
        authOptions.options.push(authOption);
    }
    return { newServiceSchemes, authOptions };
}
function makeHttpAuthRef(local, reference) {
    if (reference.type === "oauth2" && local.type === "oauth2") {
        const scopes = [];
        for (const flow of local.flows) {
            scopes.push(...flow.scopes.map((x) => x.value));
        }
        return { kind: "oauth2", auth: reference, scopes: scopes };
    }
    else if (reference.type === "noAuth") {
        return { kind: "noAuth", auth: reference };
    }
    else {
        return { kind: "any", auth: reference };
    }
}
function mergeOAuthScopes(scheme1, scheme2) {
    const flows = deepClone(scheme1.flows);
    flows.forEach((flow1, i) => {
        const flow2 = scheme2.flows[i];
        const scopes = Array.from(new Set(flow1.scopes.concat(flow2.scopes)));
        flows[i].scopes = scopes;
    });
    return {
        ...scheme1,
        flows,
    };
}
function ignoreScopes(scheme) {
    const flows = deepClone(scheme.flows);
    flows.forEach((flow) => {
        flow.scopes = [];
    });
    return {
        ...scheme,
        flows,
    };
}
function authsAreEqual(scheme1, scheme2) {
    const { model: _model1, ...withoutModel1 } = scheme1;
    const { model: _model2, ...withoutModel2 } = scheme2;
    if (withoutModel1.type === "oauth2" && withoutModel2.type === "oauth2") {
        return deepEquals(ignoreScopes(withoutModel1), ignoreScopes(withoutModel2));
    }
    return deepEquals(withoutModel1, withoutModel2);
}

/**
 * Get the responses for a given operation.
 */
function getResponsesForOperation(program, operation) {
    const diagnostics = createDiagnosticCollector();
    const responseType = operation.returnType;
    const responses = new ResponseIndex();
    if (responseType.kind === "Union") {
        for (const option of responseType.variants.values()) {
            if (isNullType(option.type)) {
                // TODO how should we treat this? https://github.com/microsoft/typespec/issues/356
                continue;
            }
            processResponseType(program, diagnostics, operation, responses, option.type);
        }
    }
    else {
        processResponseType(program, diagnostics, operation, responses, responseType);
    }
    return diagnostics.wrap(responses.values());
}
/**
 * Class keeping an index of all the response by status code
 */
class ResponseIndex {
    #index = new Map();
    get(statusCode) {
        return this.#index.get(this.#indexKey(statusCode));
    }
    set(statusCode, response) {
        this.#index.set(this.#indexKey(statusCode), response);
    }
    values() {
        return [...this.#index.values()];
    }
    #indexKey(statusCode) {
        if (typeof statusCode === "number" || statusCode === "*") {
            return String(statusCode);
        }
        else {
            return `${statusCode.start}-${statusCode.end}`;
        }
    }
}
function processResponseType(program, diagnostics, operation, responses, responseType) {
    // Get body
    let { body: resolvedBody, metadata } = diagnostics.pipe(resolveHttpPayload(program, responseType, Visibility.Read, "response"));
    // Get explicity defined status codes
    const statusCodes = diagnostics.pipe(getResponseStatusCodes(program, responseType, metadata));
    // Get response headers
    const headers = getResponseHeaders(program, metadata);
    // If there is no explicit status code, check if it should be 204
    if (statusCodes.length === 0) {
        if (isErrorModel(program, responseType)) {
            statusCodes.push("*");
        }
        else if (isVoidType(responseType)) {
            resolvedBody = undefined;
            statusCodes.push(204); // Only special case for 204 is op test(): void;
        }
        else if (resolvedBody === undefined || isVoidType(resolvedBody.type)) {
            resolvedBody = undefined;
            statusCodes.push(200);
        }
        else {
            statusCodes.push(200);
        }
    }
    // Put them into currentEndpoint.responses
    for (const statusCode of statusCodes) {
        // the first model for this statusCode/content type pair carries the
        // description for the endpoint. This could probably be improved.
        const response = responses.get(statusCode) ?? {
            statusCode: typeof statusCode === "object" ? "*" : String(statusCode),
            statusCodes: statusCode,
            type: responseType,
            description: getResponseDescription(program, operation, responseType, statusCode, metadata),
            responses: [],
        };
        if (resolvedBody !== undefined) {
            response.responses.push({
                body: resolvedBody,
                headers,
                properties: metadata,
            });
        }
        else {
            response.responses.push({ headers, properties: metadata });
        }
        responses.set(statusCode, response);
    }
}
/**
 * Get explicity defined status codes from response type and metadata
 * Return is an array of strings, possibly empty, which indicates no explicitly defined status codes.
 * We do not check for duplicates here -- that will be done by the caller.
 */
function getResponseStatusCodes(program, responseType, metadata) {
    const codes = [];
    const diagnostics = createDiagnosticCollector();
    let statusFound = false;
    for (const prop of metadata) {
        if (prop.kind === "statusCode") {
            if (statusFound) {
                reportDiagnostic(program, {
                    code: "multiple-status-codes",
                    target: responseType,
                });
            }
            statusFound = true;
            codes.push(...diagnostics.pipe(getStatusCodesWithDiagnostics(program, prop.property)));
        }
    }
    // This is only needed to retrieve the * status code set by @defaultResponse.
    // https://github.com/microsoft/typespec/issues/2485
    if (responseType.kind === "Model") {
        for (let t = responseType; t; t = t.baseModel) {
            codes.push(...getExplicitSetStatusCode(program, t));
        }
    }
    return diagnostics.wrap(codes);
}
function getExplicitSetStatusCode(program, entity) {
    return program.stateMap(HttpStateKeys.statusCode).get(entity) ?? [];
}
/**
 * Get response headers from response metadata
 */
function getResponseHeaders(program, metadata) {
    const responseHeaders = {};
    for (const prop of metadata) {
        if (prop.kind === "header") {
            responseHeaders[prop.options.name] = prop.property;
        }
    }
    return responseHeaders;
}
function isResponseEnvelope(metadata) {
    return metadata.some((prop) => prop.kind === "body" ||
        prop.kind === "bodyRoot" ||
        prop.kind === "multipartBody" ||
        prop.kind === "statusCode");
}
function getResponseDescription(program, operation, responseType, statusCode, metadata) {
    // NOTE: If the response type is an envelope and not the same as the body
    // type, then use its @doc as the response description. However, if the
    // response type is the same as the body type, then use the default status
    // code description and don't duplicate the schema description of the body
    // as the response description. This allows more freedom to change how
    // TypeSpec is expressed in semantically equivalent ways without causing
    // the output to change unnecessarily.
    if (isResponseEnvelope(metadata)) {
        const desc = getDoc(program, responseType);
        if (desc) {
            return desc;
        }
    }
    const desc = isErrorModel(program, responseType)
        ? getErrorsDoc(program, operation)
        : getReturnsDoc(program, operation);
    if (desc) {
        return desc;
    }
    return getStatusCodeDescription(statusCode);
}

/**
 * Return the Http Operation details for a given TypeSpec operation.
 * @param operation Operation
 * @param options Optional option on how to resolve the http details.
 */
function getHttpOperation(program, operation, options) {
    return getHttpOperationInternal(program, operation, options, new Map());
}
/**
 * Get all the Http Operation in the given container.
 * @param program Program
 * @param container Namespace or interface containing operations
 * @param options Resolution options
 * @returns
 */
function listHttpOperationsIn(program, container, options) {
    const diagnostics = createDiagnosticCollector();
    const operations = listOperationsIn(container, options?.listOptions);
    const cache = new Map();
    const httpOperations = operations.map((x) => diagnostics.pipe(getHttpOperationInternal(program, x, options, cache)));
    return diagnostics.wrap(httpOperations);
}
/**
 * Returns all the services defined.
 */
function getAllHttpServices(program, options) {
    const diagnostics = createDiagnosticCollector();
    const serviceNamespaces = listServices(program);
    const services = serviceNamespaces.map((x) => diagnostics.pipe(getHttpService(program, x.type, options)));
    if (serviceNamespaces.length === 0) {
        services.push(diagnostics.pipe(getHttpService(program, program.getGlobalNamespaceType(), options)));
    }
    return diagnostics.wrap(services);
}
function getHttpService(program, serviceNamespace, options) {
    const diagnostics = createDiagnosticCollector();
    const httpOperations = diagnostics.pipe(listHttpOperationsIn(program, serviceNamespace, {
        ...options,
        listOptions: {
            recursive: serviceNamespace !== program.getGlobalNamespaceType(),
        },
    }));
    const authentication = getAuthentication(program, serviceNamespace);
    validateProgram(program, diagnostics);
    validateRouteUnique(program, diagnostics, httpOperations);
    const service = {
        namespace: serviceNamespace,
        operations: httpOperations,
        authentication: authentication,
    };
    return diagnostics.wrap(service);
}
/**
 * @deprecated use `getAllHttpServices` instead
 */
function getAllRoutes(program, options) {
    const [services, diagnostics] = getAllHttpServices(program, options);
    return [services[0].operations, diagnostics];
}
function reportIfNoRoutes(program, routes) {
    if (routes.length === 0) {
        navigateProgram(program, {
            namespace: (namespace) => {
                if (namespace.operations.size > 0) {
                    reportDiagnostic(program, {
                        code: "no-service-found",
                        format: {
                            namespace: namespace.name,
                        },
                        target: namespace,
                    });
                }
            },
        });
    }
}
function validateRouteUnique(program, diagnostics, operations) {
    const grouped = new Map();
    for (const operation of operations) {
        const { verb, path } = operation;
        if (operation.overloading !== undefined && isOverloadSameEndpoint(operation)) {
            continue;
        }
        if (isSharedRoute(program, operation.operation)) {
            continue;
        }
        let map = grouped.get(path);
        if (map === undefined) {
            map = new Map();
            grouped.set(path, map);
        }
        let list = map.get(verb);
        if (list === undefined) {
            list = [];
            map.set(verb, list);
        }
        list.push(operation);
    }
    for (const [path, map] of grouped) {
        for (const [verb, routes] of map) {
            if (routes.length >= 2) {
                for (const route of routes) {
                    diagnostics.add(createDiagnostic({
                        code: "duplicate-operation",
                        format: { path, verb, operationName: route.operation.name },
                        target: route.operation,
                    }));
                }
            }
        }
    }
}
function isOverloadSameEndpoint(overload) {
    return overload.path === overload.overloading.path && overload.verb === overload.overloading.verb;
}
function getHttpOperationInternal(program, operation, options, cache) {
    const existing = cache.get(operation);
    if (existing) {
        return [existing, []];
    }
    const diagnostics = createDiagnosticCollector();
    const httpOperationRef = { operation };
    cache.set(operation, httpOperationRef);
    const overloadBase = getOverloadedOperation(program, operation);
    let overloading;
    if (overloadBase) {
        overloading = httpOperationRef.overloading = diagnostics.pipe(getHttpOperationInternal(program, overloadBase, options, cache));
    }
    const route = diagnostics.pipe(resolvePathAndParameters(program, operation, overloading, options ?? {}));
    const responses = diagnostics.pipe(getResponsesForOperation(program, operation));
    const authentication = getAuthenticationForOperation(program, operation);
    const httpOperation = {
        path: route.path,
        uriTemplate: route.uriTemplate,
        pathSegments: [],
        verb: route.parameters.verb,
        container: operation.interface ?? operation.namespace ?? program.getGlobalNamespaceType(),
        parameters: route.parameters,
        responses,
        operation,
        authentication,
    };
    Object.assign(httpOperationRef, httpOperation);
    const overloads = getOverloads(program, operation);
    if (overloads) {
        httpOperationRef.overloads = overloads.map((x) => diagnostics.pipe(getHttpOperationInternal(program, x, options, cache)));
    }
    return diagnostics.wrap(httpOperationRef);
}
function validateProgram(program, diagnostics) {
    navigateProgram(program, {
        modelProperty(property) {
            checkForUnsupportedVisibility(property);
        },
    });
    // NOTE: This is intentionally not checked in the visibility decorator
    // itself as that would be a layering violation, putting a REST
    // interpretation of visibility into the core.
    function checkForUnsupportedVisibility(property) {
        // eslint-disable-next-line @typescript-eslint/no-deprecated
        if (getVisibility(program, property)?.includes("write")) {
            // NOTE: Check for name equality instead of function equality
            // to deal with multiple copies of core being used.
            const decorator = property.decorators.find((d) => d.decorator.name === $visibility.name);
            const arg = decorator?.args.find((a) => a.node?.kind === SyntaxKind.StringLiteral && a.node.value === "write");
            const target = arg?.node ?? property;
            diagnostics.add(createDiagnostic({ code: "write-visibility-not-supported", target }));
        }
    }
}

function $onValidate(program) {
    // Pass along any diagnostics that might be returned from the HTTP library
    const [services, diagnostics] = getAllHttpServices(program);
    if (diagnostics.length > 0) {
        program.reportDiagnostics(diagnostics);
    }
    validateSharedRouteConsistency(program, services);
    validateHttpFiles(program);
}
function validateHttpFiles(program) {
    const httpFiles = [...program.stateSet(HttpStateKeys.file)];
    for (const model of httpFiles) {
        if (model.kind === "Model") {
            validateHttpFileModel(program, model);
        }
    }
}
function validateHttpFileModel(program, model) {
    for (const prop of model.properties.values()) {
        if (prop.name !== "contentType" && prop.name !== "filename" && prop.name !== "contents") {
            reportDiagnostic(program, {
                code: "http-file-extra-property",
                format: { propName: prop.name },
                target: prop,
            });
        }
    }
    for (const child of model.derivedModels) {
        validateHttpFileModel(program, child);
    }
}
function groupHttpOperations(operations) {
    const paths = new Map();
    for (const operation of operations) {
        const { verb, path } = operation;
        let pathOps = paths.get(path);
        if (pathOps === undefined) {
            pathOps = new Map();
            paths.set(path, pathOps);
        }
        const ops = pathOps.get(verb);
        if (ops === undefined) {
            pathOps.set(verb, [operation]);
        }
        else {
            ops.push(operation);
        }
    }
    return paths;
}
function validateSharedRouteConsistency(program, services) {
    for (const service of services) {
        const paths = groupHttpOperations(service.operations);
        for (const pathOps of paths.values()) {
            for (const ops of pathOps.values()) {
                let hasShared = false;
                let hasNonShared = false;
                for (const op of ops) {
                    if (isSharedRoute(program, op.operation)) {
                        hasShared = true;
                    }
                    else {
                        hasNonShared = true;
                    }
                }
                if (hasShared && hasNonShared) {
                    for (const op of ops) {
                        reportDiagnostic(program, {
                            code: "shared-inconsistency",
                            target: op.operation,
                            format: { verb: op.verb, path: op.path },
                        });
                    }
                }
            }
        }
    }
}

/** @internal */
const $decorators = {
    "TypeSpec.Http": {
        body: $body,
        bodyIgnore: $bodyIgnore,
        bodyRoot: $bodyRoot,
        cookie: $cookie,
        delete: $delete,
        get: $get,
        header: $header,
        head: $head,
        includeInapplicableMetadataInPayload: $includeInapplicableMetadataInPayload,
        multipartBody: $multipartBody,
        patch: $patch,
        path: $path,
        post: $post,
        put: $put,
        query: $query,
        route: $route,
        server: $server,
        sharedRoute: $sharedRoute,
        statusCode: $statusCode,
        useAuth: $useAuth,
    },
};

var f1 = /*#__PURE__*/Object.freeze({
    __proto__: null,
    $decorators: $decorators,
    $lib: $lib,
    $onValidate: $onValidate
});

var f0 = /*#__PURE__*/Object.freeze({
    __proto__: null,
    $body: $body,
    $bodyIgnore: $bodyIgnore,
    $bodyRoot: $bodyRoot,
    $cookie: $cookie,
    $decorators: $decorators,
    $delete: $delete,
    $get: $get,
    $head: $head,
    $header: $header,
    $includeInapplicableMetadataInPayload: $includeInapplicableMetadataInPayload,
    $lib: $lib,
    $linter: $linter,
    $multipartBody: $multipartBody,
    $patch: $patch,
    $path: $path,
    $post: $post,
    $put: $put,
    $query: $query,
    $route: $route,
    $server: $server,
    $sharedRoute: $sharedRoute,
    $statusCode: $statusCode,
    $useAuth: $useAuth,
    DefaultRouteProducer: DefaultRouteProducer,
    get Visibility () { return Visibility; },
    addQueryParamsToUriTemplate: addQueryParamsToUriTemplate,
    createMetadataInfo: createMetadataInfo,
    getAllHttpServices: getAllHttpServices,
    getAllRoutes: getAllRoutes,
    getAuthentication: getAuthentication,
    getAuthenticationForOperation: getAuthenticationForOperation,
    getContentTypes: getContentTypes,
    getCookieParamOptions: getCookieParamOptions,
    getHeaderFieldName: getHeaderFieldName,
    getHeaderFieldOptions: getHeaderFieldOptions,
    getHttpFileModel: getHttpFileModel,
    getHttpOperation: getHttpOperation,
    getHttpPart: getHttpPart,
    getHttpService: getHttpService,
    getOperationParameters: getOperationParameters,
    getOperationVerb: getOperationVerb,
    getPathParamName: getPathParamName,
    getPathParamOptions: getPathParamOptions,
    getQueryParamName: getQueryParamName,
    getQueryParamOptions: getQueryParamOptions,
    getRequestVisibility: getRequestVisibility,
    getResponsesForOperation: getResponsesForOperation,
    getRouteOptionsForNamespace: getRouteOptionsForNamespace,
    getRoutePath: getRoutePath,
    getRouteProducer: getRouteProducer,
    getServers: getServers,
    getStatusCodeDescription: getStatusCodeDescription,
    getStatusCodes: getStatusCodes,
    getStatusCodesWithDiagnostics: getStatusCodesWithDiagnostics,
    getUriTemplatePathParam: getUriTemplatePathParam,
    getVisibilitySuffix: getVisibilitySuffix,
    includeInapplicableMetadataInPayload: includeInapplicableMetadataInPayload,
    includeInterfaceRoutesInNamespace: includeInterfaceRoutesInNamespace,
    isApplicableMetadata: isApplicableMetadata,
    isApplicableMetadataOrBody: isApplicableMetadataOrBody,
    isBody: isBody,
    isBodyIgnore: isBodyIgnore,
    isBodyRoot: isBodyRoot,
    isContentTypeHeader: isContentTypeHeader,
    isCookieParam: isCookieParam,
    isHeader: isHeader,
    isHttpFile: isHttpFile,
    isMetadata: isMetadata,
    isMultipartBodyProperty: isMultipartBodyProperty,
    isOrExtendsHttpFile: isOrExtendsHttpFile,
    isOverloadSameEndpoint: isOverloadSameEndpoint,
    isPathParam: isPathParam,
    isQueryParam: isQueryParam,
    isSharedRoute: isSharedRoute,
    isStatusCode: isStatusCode,
    isVisible: isVisible,
    joinPathSegments: joinPathSegments,
    listHttpOperationsIn: listHttpOperationsIn,
    namespace: namespace$1,
    reportIfNoRoutes: reportIfNoRoutes,
    resolveAuthentication: resolveAuthentication,
    resolvePathAndParameters: resolvePathAndParameters,
    resolveRequestVisibility: resolveRequestVisibility,
    setAuthentication: setAuthentication,
    setRoute: setRoute,
    setRouteOptionsForNamespace: setRouteOptionsForNamespace,
    setRouteProducer: setRouteProducer,
    setSharedRoute: setSharedRoute,
    setStatusCode: setStatusCode,
    validateRouteUnique: validateRouteUnique
});

const TypeSpecJSSources = {
"dist/src/index.js": f0,
"dist/src/tsp-index.js": f1,
"dist/src/private.decorators.js": f2,
};
const TypeSpecSources = {
  "package.json": "{\"name\":\"@typespec/http\",\"version\":\"0.64.0\",\"author\":\"Microsoft Corporation\",\"description\":\"TypeSpec HTTP protocol binding\",\"homepage\":\"https://github.com/microsoft/typespec\",\"docusaurusWebsite\":\"https://typespec.io/docs\",\"readme\":\"https://github.com/microsoft/typespec/blob/main/README.md\",\"license\":\"MIT\",\"repository\":{\"type\":\"git\",\"url\":\"git+https://github.com/microsoft/typespec.git\"},\"bugs\":{\"url\":\"https://github.com/microsoft/typespec/issues\"},\"keywords\":[\"typespec\"],\"type\":\"module\",\"main\":\"dist/src/index.js\",\"tspMain\":\"lib/http.tsp\",\"exports\":{\".\":{\"typespec\":\"./lib/http.tsp\",\"types\":\"./dist/src/index.d.ts\",\"default\":\"./dist/src/index.js\"},\"./testing\":{\"types\":\"./dist/src/testing/index.d.ts\",\"default\":\"./dist/src/testing/index.js\"},\"./streams\":{\"typespec\":\"./lib/streams/main.tsp\",\"types\":\"./dist/src/streams/index.d.ts\",\"default\":\"./dist/src/streams/index.js\"},\"./experimental\":{\"types\":\"./dist/src/experimental/index.d.ts\",\"default\":\"./dist/src/experimental/index.js\"}},\"engines\":{\"node\":\">=18.0.0\"},\"scripts\":{\"clean\":\"rimraf ./dist ./temp\",\"build\":\"npm run gen-extern-signature && tsc -p . && npm run lint-typespec-library\",\"watch\":\"tsc -p . --watch\",\"gen-extern-signature\":\"tspd --enable-experimental gen-extern-signature .\",\"lint-typespec-library\":\"tsp compile . --warn-as-error --import @typespec/library-linter --no-emit\",\"test\":\"vitest run\",\"test:watch\":\"vitest -w\",\"test:ui\":\"vitest --ui\",\"test:ci\":\"vitest run --coverage --reporter=junit --reporter=default\",\"lint\":\"eslint . --max-warnings=0\",\"lint:fix\":\"eslint . --fix\",\"regen-docs\":\"tspd doc .  --enable-experimental  --output-dir ../../website/src/content/docs/docs/libraries/http/reference\"},\"files\":[\"lib/**/*.tsp\",\"dist/**\",\"!dist/test/**\"],\"peerDependencies\":{\"@typespec/compiler\":\"workspace:~\",\"@typespec/streams\":\"workspace:~\"},\"peerDependenciesMeta\":{\"@typespec/streams\":{\"optional\":true}},\"devDependencies\":{\"@types/node\":\"~22.7.9\",\"@typespec/compiler\":\"workspace:~\",\"@typespec/library-linter\":\"workspace:~\",\"@typespec/streams\":\"workspace:~\",\"@typespec/tspd\":\"workspace:~\",\"@vitest/coverage-v8\":\"^2.1.5\",\"@vitest/ui\":\"^2.1.2\",\"c8\":\"^10.1.2\",\"rimraf\":\"~6.0.1\",\"typescript\":\"~5.6.3\",\"vitest\":\"^2.1.5\"}}",
  "../compiler/lib/intrinsics.tsp": "import \"../dist/src/lib/intrinsic/tsp-index.js\";\nimport \"./prototypes.tsp\";\n\n// This file contains all the intrinsic types of typespec. Everything here will always be loaded\nnamespace TypeSpec;\n\n/**\n * Represent a byte array\n */\nscalar bytes;\n\n/**\n * A numeric type\n */\nscalar numeric;\n\n/**\n * A whole number. This represent any `integer` value possible.\n * It is commonly represented as `BigInteger` in some languages.\n */\nscalar integer extends numeric;\n\n/**\n * A number with decimal value\n */\nscalar float extends numeric;\n\n/**\n * A 64-bit integer. (`-9,223,372,036,854,775,808` to `9,223,372,036,854,775,807`)\n */\nscalar int64 extends integer;\n\n/**\n * A 32-bit integer. (`-2,147,483,648` to `2,147,483,647`)\n */\nscalar int32 extends int64;\n\n/**\n * A 16-bit integer. (`-32,768` to `32,767`)\n */\nscalar int16 extends int32;\n\n/**\n * A 8-bit integer. (`-128` to `127`)\n */\nscalar int8 extends int16;\n\n/**\n * A 64-bit unsigned integer (`0` to `18,446,744,073,709,551,615`)\n */\nscalar uint64 extends integer;\n\n/**\n * A 32-bit unsigned integer (`0` to `4,294,967,295`)\n */\nscalar uint32 extends uint64;\n\n/**\n * A 16-bit unsigned integer (`0` to `65,535`)\n */\nscalar uint16 extends uint32;\n\n/**\n * A 8-bit unsigned integer (`0` to `255`)\n */\nscalar uint8 extends uint16;\n\n/**\n * An integer that can be serialized to JSON (`−9007199254740991 (−(2^53 − 1))` to `9007199254740991 (2^53 − 1)` )\n */\nscalar safeint extends int64;\n\n/**\n * A 64 bit floating point number. (`±5.0 × 10^−324` to `±1.7 × 10^308`)\n */\nscalar float64 extends float;\n\n/**\n * A 32 bit floating point number. (`±1.5 x 10^−45` to `±3.4 x 10^38`)\n */\nscalar float32 extends float64;\n\n/**\n * A decimal number with any length and precision. This represent any `decimal` value possible.\n * It is commonly represented as `BigDecimal` in some languages.\n */\nscalar decimal extends numeric;\n\n/**\n * A 128-bit decimal number.\n */\nscalar decimal128 extends decimal;\n\n/**\n * A sequence of textual characters.\n */\nscalar string;\n\n/**\n * A date on a calendar without a time zone, e.g. \"April 10th\"\n */\nscalar plainDate {\n  /**\n   * Create a plain date from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = plainTime.fromISO(\"2024-05-06\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * A time on a clock without a time zone, e.g. \"3:00 am\"\n */\nscalar plainTime {\n  /**\n   * Create a plain time from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = plainTime.fromISO(\"12:34\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * An instant in coordinated universal time (UTC)\"\n */\nscalar utcDateTime {\n  /**\n   * Create a date from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = utcDateTime.fromISO(\"2024-05-06T12:20-12Z\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * A date and time in a particular time zone, e.g. \"April 10th at 3:00am in PST\"\n */\nscalar offsetDateTime {\n  /**\n   * Create a date from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = offsetDateTime.fromISO(\"2024-05-06T12:20-12-0700\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * A duration/time period. e.g 5s, 10h\n */\nscalar duration {\n  /**\n   * Create a duration from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = duration.fromISO(\"P1Y1D\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * Boolean with `true` and `false` values.\n */\nscalar boolean;\n\n/**\n * @dev Array model type, equivalent to `Element[]`\n * @template Element The type of the array elements\n */\n@indexer(integer, Element)\nmodel Array<Element> {}\n\n/**\n * @dev Model with string properties where all the properties have type `Property`\n * @template Element The type of the properties\n */\n@indexer(string, Element)\nmodel Record<Element> {}\n",
  "../compiler/lib/prototypes.tsp": "namespace TypeSpec.Prototypes;\n\nextern dec getter(target: unknown);\n\nnamespace Types {\n  interface ModelProperty {\n    @getter type(): unknown;\n  }\n\n  interface Operation {\n    @getter returnType(): unknown;\n    @getter parameters(): unknown;\n  }\n\n  interface Array<TElementType> {\n    @getter elementType(): TElementType;\n  }\n}\n",
  "../compiler/lib/std/main.tsp": "// TypeSpec standard library. Everything in here can be omitted by using `--nostdlib` cli flag or `nostdlib` in the config.\nimport \"./types.tsp\";\nimport \"./decorators.tsp\";\nimport \"./reflection.tsp\";\nimport \"./projected-names.tsp\";\nimport \"./visibility.tsp\";\n",
  "../compiler/lib/std/types.tsp": "namespace TypeSpec;\n\n/**\n * Represent a 32-bit unix timestamp datetime with 1s of granularity.\n * It measures time by the number of seconds that have elapsed since 00:00:00 UTC on 1 January 1970.\n */\n@encode(\"unixTimestamp\", int32)\nscalar unixTimestamp32 extends utcDateTime;\n\n/**\n * Represent a model\n */\n// Deprecated June 2023 sprint\n#deprecated \"object is deprecated. Please use {} for an empty model, `Record<unknown>` for a record with unknown property types, `unknown[]` for an array.\"\nmodel object {}\n\n/**\n * Represent a URL string as described by https://url.spec.whatwg.org/\n */\nscalar url extends string;\n\n/**\n * Represents a collection of optional properties.\n *\n * @template Source An object whose spread properties are all optional.\n */\n@doc(\"The template for adding optional properties.\")\n@withOptionalProperties\nmodel OptionalProperties<Source> {\n  ...Source;\n}\n\n/**\n * Represents a collection of updateable properties.\n *\n * @template Source An object whose spread properties are all updateable.\n */\n@doc(\"The template for adding updateable properties.\")\n@withUpdateableProperties\nmodel UpdateableProperties<Source> {\n  ...Source;\n}\n\n/**\n * Represents a collection of omitted properties.\n *\n * @template Source An object whose properties are spread.\n * @template Keys The property keys to omit.\n */\n@doc(\"The template for omitting properties.\")\n@withoutOmittedProperties(Keys)\nmodel OmitProperties<Source, Keys extends string> {\n  ...Source;\n}\n\n/**\n * Represents a collection of properties with only the specified keys included.\n *\n * @template Source An object whose properties are spread.\n * @template Keys The property keys to include.\n */\n@doc(\"The template for picking properties.\")\n@withPickedProperties(Keys)\nmodel PickProperties<Source, Keys extends string> {\n  ...Source;\n}\n\n/**\n * Represents a collection of properties with default values omitted.\n *\n * @template Source An object whose spread property defaults are all omitted.\n */\n@withoutDefaultValues\nmodel OmitDefaults<Source> {\n  ...Source;\n}\n\n/**\n * Applies a visibility setting to a collection of properties.\n *\n * @template Source An object whose properties are spread.\n * @template Visibility The visibility to apply to all properties.\n */\n@doc(\"The template for setting the default visibility of key properties.\")\n@withDefaultKeyVisibility(Visibility)\nmodel DefaultKeyVisibility<Source, Visibility extends valueof string> {\n  ...Source;\n}\n",
  "../compiler/lib/std/decorators.tsp": "import \"../../dist/src/lib/tsp-index.js\";\n\nusing TypeSpec.Reflection;\n\nnamespace TypeSpec;\n\n/**\n * Typically a short, single-line description.\n * @param summary Summary string.\n *\n * @example\n * ```typespec\n * @summary(\"This is a pet\")\n * model Pet {}\n * ```\n */\nextern dec summary(target: unknown, summary: valueof string);\n\n/**\n * Attach a documentation string.\n * @param doc Documentation string\n * @param formatArgs Record with key value pair that can be interpolated in the doc.\n *\n * @example\n * ```typespec\n * @doc(\"Represent a Pet available in the PetStore\")\n * model Pet {}\n * ```\n */\nextern dec doc(target: unknown, doc: valueof string, formatArgs?: {});\n\n/**\n * Attach a documentation string to describe the successful return types of an operation.\n * If an operation returns a union of success and errors it only describes the success. See `@errorsDoc` for error documentation.\n * @param doc Documentation string\n *\n * @example\n * ```typespec\n * @returnsDoc(\"Returns doc\")\n * op get(): Pet | NotFound;\n * ```\n */\nextern dec returnsDoc(target: Operation, doc: valueof string);\n\n/**\n * Attach a documentation string to describe the error return types of an operation.\n * If an operation returns a union of success and errors it only describes the errors. See `@returnsDoc` for success documentation.\n * @param doc Documentation string\n *\n * @example\n * ```typespec\n * @errorsDoc(\"Errors doc\")\n * op get(): Pet | NotFound;\n * ```\n */\nextern dec errorsDoc(target: Operation, doc: valueof string);\n\n/**\n * Mark this type as deprecated.\n *\n * NOTE: This decorator **should not** be used, use the `#deprecated` directive instead.\n *\n * @deprecated Use the `#deprecated` [directive](https://typespec.io/docs/language-basics/directives/#deprecated) instead.\n * @param message Deprecation message.\n *\n * @example\n *\n * Use the `#deprecated` directive instead:\n *\n * ```typespec\n * #deprecated \"Use ActionV2\"\n * op Action<Result>(): Result;\n * ```\n */\n#deprecated \"@deprecated decorator is deprecated. Use the `#deprecated` directive instead.\"\nextern dec deprecated(target: unknown, message: valueof string);\n\n/**\n * Service options.\n */\nmodel ServiceOptions {\n  /**\n   * Title of the service.\n   */\n  title?: string;\n\n  /**\n   * Version of the service.\n   */\n  version?: string;\n}\n\n/**\n * Mark this namespace as describing a service and configure service properties.\n * @param options Optional configuration for the service.\n *\n * @example\n * ```typespec\n * @service\n * namespace PetStore;\n * ```\n *\n * @example Setting service title\n * ```typespec\n * @service({title: \"Pet store\"})\n * namespace PetStore;\n * ```\n *\n * @example Setting service version\n * ```typespec\n * @service({version: \"1.0\"})\n * namespace PetStore;\n * ```\n */\nextern dec service(target: Namespace, options?: ServiceOptions);\n\n/**\n * Specify that this model is an error type. Operations return error types when the operation has failed.\n *\n * @example\n * ```typespec\n * @error\n * model PetStoreError {\n *   code: string;\n *   message: string;\n * }\n * ```\n */\nextern dec error(target: Model);\n\n/**\n * Specify a known data format hint for this string type. For example `uuid`, `uri`, etc.\n * This differs from the `@pattern` decorator which is meant to specify a regular expression while `@format` accepts a known format name.\n * The format names are open ended and are left to emitter to interpret.\n *\n * @param format format name.\n *\n * @example\n * ```typespec\n * @format(\"uuid\")\n * scalar uuid extends string;\n * ```\n */\nextern dec format(target: string | bytes | ModelProperty, format: valueof string);\n\n/**\n * Specify the the pattern this string should respect using simple regular expression syntax.\n * The following syntax is allowed: alternations (`|`), quantifiers (`?`, `*`, `+`, and `{ }`), wildcard (`.`), and grouping parentheses.\n * Advanced features like look-around, capture groups, and references are not supported.\n *\n * This decorator may optionally provide a custom validation _message_. Emitters may choose to use the message to provide\n * context when pattern validation fails. For the sake of consistency, the message should be a phrase that describes in\n * plain language what sort of content the pattern attempts to validate. For example, a complex regular expression that\n * validates a GUID string might have a message like \"Must be a valid GUID.\"\n *\n * @param pattern Regular expression.\n * @param validationMessage Optional validation message that may provide context when validation fails.\n *\n * @example\n * ```typespec\n * @pattern(\"[a-z]+\", \"Must be a string consisting of only lower case letters and of at least one character.\")\n * scalar LowerAlpha extends string;\n * ```\n */\nextern dec pattern(\n  target: string | bytes | ModelProperty,\n  pattern: valueof string,\n  validationMessage?: valueof string\n);\n\n/**\n * Specify the minimum length this string type should be.\n * @param value Minimum length\n *\n * @example\n * ```typespec\n * @minLength(2)\n * scalar Username extends string;\n * ```\n */\nextern dec minLength(target: string | ModelProperty, value: valueof integer);\n\n/**\n * Specify the maximum length this string type should be.\n * @param value Maximum length\n *\n * @example\n * ```typespec\n * @maxLength(20)\n * scalar Username extends string;\n * ```\n */\nextern dec maxLength(target: string | ModelProperty, value: valueof integer);\n\n/**\n * Specify the minimum number of items this array should have.\n * @param value Minimum number\n *\n * @example\n * ```typespec\n * @minItems(1)\n * model Endpoints is string[];\n * ```\n */\nextern dec minItems(target: unknown[] | ModelProperty, value: valueof integer);\n\n/**\n * Specify the maximum number of items this array should have.\n * @param value Maximum number\n *\n * @example\n * ```typespec\n * @maxItems(5)\n * model Endpoints is string[];\n * ```\n */\nextern dec maxItems(target: unknown[] | ModelProperty, value: valueof integer);\n\n/**\n * Specify the minimum value this numeric type should be.\n * @param value Minimum value\n *\n * @example\n * ```typespec\n * @minValue(18)\n * scalar Age is int32;\n * ```\n */\nextern dec minValue(target: numeric | ModelProperty, value: valueof numeric);\n\n/**\n * Specify the maximum value this numeric type should be.\n * @param value Maximum value\n *\n * @example\n * ```typespec\n * @maxValue(200)\n * scalar Age is int32;\n * ```\n */\nextern dec maxValue(target: numeric | ModelProperty, value: valueof numeric);\n\n/**\n * Specify the minimum value this numeric type should be, exclusive of the given\n * value.\n * @param value Minimum value\n *\n * @example\n * ```typespec\n * @minValueExclusive(0)\n * scalar distance is float64;\n * ```\n */\nextern dec minValueExclusive(target: numeric | ModelProperty, value: valueof numeric);\n\n/**\n * Specify the maximum value this numeric type should be, exclusive of the given\n * value.\n * @param value Maximum value\n *\n * @example\n * ```typespec\n * @maxValueExclusive(50)\n * scalar distance is float64;\n * ```\n */\nextern dec maxValueExclusive(target: numeric | ModelProperty, value: valueof numeric);\n\n/**\n * Mark this string as a secret value that should be treated carefully to avoid exposure\n *\n * @example\n * ```typespec\n * @secret\n * scalar Password is string;\n * ```\n */\nextern dec secret(target: string | ModelProperty);\n\n/**\n * Attaches a tag to an operation, interface, or namespace. Multiple `@tag` decorators can be specified to attach multiple tags to a TypeSpec element.\n * @param tag Tag value\n */\nextern dec tag(target: Namespace | Interface | Operation, tag: valueof string);\n\n/**\n * Specifies how a templated type should name their instances.\n * @param name name the template instance should take\n * @param formatArgs Model with key value used to interpolate the name\n *\n * @example\n * ```typespec\n * @friendlyName(\"{name}List\", T)\n * model List<Item> {\n *   value: Item[];\n *   nextLink: string;\n * }\n * ```\n */\nextern dec friendlyName(target: unknown, name: valueof string, formatArgs?: unknown);\n\n/**\n * Provide a set of known values to a string type.\n * @param values Known values enum.\n *\n * @example\n * ```typespec\n * @knownValues(KnownErrorCode)\n * scalar ErrorCode extends string;\n *\n * enum KnownErrorCode {\n *   NotFound,\n *   Invalid,\n * }\n * ```\n */\n#deprecated \"This decorator has been deprecated. Use a named union of string literals with a string variant to achieve the same result without a decorator.\"\nextern dec knownValues(target: string | numeric | ModelProperty, values: Enum);\n\n/**\n * Mark a model property as the key to identify instances of that type\n * @param altName Name of the property. If not specified, the decorated property name is used.\n *\n * @example\n * ```typespec\n * model Pet {\n *   @key id: string;\n * }\n * ```\n */\nextern dec key(target: ModelProperty, altName?: valueof string);\n\n/**\n * Specify this operation is an overload of the given operation.\n * @param overloadbase Base operation that should be a union of all overloads\n *\n * @example\n * ```typespec\n * op upload(data: string | bytes, @header contentType: \"text/plain\" | \"application/octet-stream\"): void;\n * @overload(upload)\n * op uploadString(data: string, @header contentType: \"text/plain\" ): void;\n * @overload(upload)\n * op uploadBytes(data: bytes, @header contentType: \"application/octet-stream\"): void;\n * ```\n */\nextern dec overload(target: Operation, overloadbase: Operation);\n\n/**\n * DEPRECATED: Use `@encodedName` instead.\n *\n * Provide an alternative name for this type.\n * @param targetName Projection target\n * @param projectedName Alternative name\n *\n * @example\n * ```typespec\n * model Certificate {\n *   @projectedName(\"json\", \"exp\")\n *   expireAt: int32;\n * }\n * ```\n */\n#deprecated \"Use `@encodedName` instead for changing the name over the wire.\"\nextern dec projectedName(\n  target: unknown,\n  targetName: valueof string,\n  projectedName: valueof string\n);\n\n/**\n * Provide an alternative name for this type when serialized to the given mime type.\n * @param mimeType Mime type this should apply to. The mime type should be a known mime type as described here https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types without any suffix (e.g. `+json`)\n * @param name Alternative name\n *\n * @example\n *\n * ```typespec\n * model Certificate {\n *   @encodedName(\"application/json\", \"exp\")\n *   @encodedName(\"application/xml\", \"expiry\")\n *   expireAt: int32;\n * }\n * ```\n *\n * @example Invalid values\n *\n * ```typespec\n * @encodedName(\"application/merge-patch+json\", \"exp\")\n *              ^ error cannot use subtype\n * ```\n */\nextern dec encodedName(target: unknown, mimeType: valueof string, name: valueof string);\n\n/**\n * Specify the property to be used to discriminate this type.\n * @param propertyName The property name to use for discrimination\n *\n * @example\n *\n * ```typespec\n * @discriminator(\"kind\")\n * union Pet{ cat: Cat, dog: Dog }\n *\n * model Cat {kind: \"cat\", meow: boolean}\n * model Dog {kind: \"dog\", bark: boolean}\n * ```\n *\n * ```typespec\n * @discriminator(\"kind\")\n * model Pet{ kind: string }\n *\n * model Cat extends Pet {kind: \"cat\", meow: boolean}\n * model Dog extends Pet  {kind: \"dog\", bark: boolean}\n * ```\n */\nextern dec discriminator(target: Model | Union, propertyName: valueof string);\n\n/**\n * Known encoding to use on utcDateTime or offsetDateTime\n */\nenum DateTimeKnownEncoding {\n  /**\n   * RFC 3339 standard. https://www.ietf.org/rfc/rfc3339.txt\n   * Encode to string.\n   */\n  rfc3339: \"rfc3339\",\n\n  /**\n   * RFC 7231 standard. https://www.ietf.org/rfc/rfc7231.txt\n   * Encode to string.\n   */\n  rfc7231: \"rfc7231\",\n\n  /**\n   * Encode a datetime to a unix timestamp.\n   * Unix timestamps are represented as an integer number of seconds since the Unix epoch and usually encoded as an int32.\n   */\n  unixTimestamp: \"unixTimestamp\",\n}\n\n/**\n * Known encoding to use on duration\n */\nenum DurationKnownEncoding {\n  /**\n   * ISO8601 duration\n   */\n  ISO8601: \"ISO8601\",\n\n  /**\n   * Encode to integer or float\n   */\n  seconds: \"seconds\",\n}\n\n/**\n * Known encoding to use on bytes\n */\nenum BytesKnownEncoding {\n  /**\n   * Encode to Base64\n   */\n  base64: \"base64\",\n\n  /**\n   * Encode to Base64 Url\n   */\n  base64url: \"base64url\",\n}\n\n/**\n * Encoding for serializing arrays\n */\nenum ArrayEncoding {\n  /** Each values of the array is separated by a | */\n  pipeDelimited,\n\n  /** Each values of the array is separated by a <space> */\n  spaceDelimited,\n}\n\n/**\n * Specify how to encode the target type.\n * @param encodingOrEncodeAs Known name of an encoding or a scalar type to encode as(Only for numeric types to encode as string).\n * @param encodedAs What target type is this being encoded as. Default to string.\n *\n * @example offsetDateTime encoded with rfc7231\n *\n * ```tsp\n * @encode(\"rfc7231\")\n * scalar myDateTime extends offsetDateTime;\n * ```\n *\n * @example utcDateTime encoded with unixTimestamp\n *\n * ```tsp\n * @encode(\"unixTimestamp\", int32)\n * scalar myDateTime extends unixTimestamp;\n * ```\n *\n * @example encode numeric type to string\n *\n * ```tsp\n * model Pet {\n *   @encode(string) id: int64;\n * }\n * ```\n */\nextern dec encode(\n  target: Scalar | ModelProperty,\n  encodingOrEncodeAs: (valueof string | EnumMember) | Scalar,\n  encodedAs?: Scalar\n);\n\n/** Options for example decorators */\nmodel ExampleOptions {\n  /** The title of the example */\n  title?: string;\n\n  /** Description of the example */\n  description?: string;\n}\n\n/**\n * Provide an example value for a data type.\n *\n * @param example Example value.\n * @param options Optional metadata for the example.\n *\n * @example\n *\n * ```tsp\n * @example(#{name: \"Fluffy\", age: 2})\n * model Pet {\n *  name: string;\n *  age: int32;\n * }\n * ```\n */\nextern dec example(\n  target: Model | Enum | Scalar | Union | ModelProperty | UnionVariant,\n  example: valueof unknown,\n  options?: valueof ExampleOptions\n);\n\n/**\n * Operation example configuration.\n */\nmodel OperationExample {\n  /** Example request body. */\n  parameters?: unknown;\n\n  /** Example response body. */\n  returnType?: unknown;\n}\n\n/**\n * Provide example values for an operation's parameters and corresponding return type.\n *\n * @param example Example value.\n * @param options Optional metadata for the example.\n *\n * @example\n *\n * ```tsp\n * @opExample(#{parameters: #{name: \"Fluffy\", age: 2}, returnType: #{name: \"Fluffy\", age: 2, id: \"abc\"})\n * op createPet(pet: Pet): Pet;\n * ```\n */\nextern dec opExample(\n  target: Operation,\n  example: valueof OperationExample,\n  options?: valueof ExampleOptions\n);\n\n/**\n * Returns the model with required properties removed.\n */\nextern dec withOptionalProperties(target: Model);\n\n/**\n * Returns the model with any default values removed.\n */\nextern dec withoutDefaultValues(target: Model);\n\n/**\n * Returns the model with the given properties omitted.\n * @param omit List of properties to omit\n */\nextern dec withoutOmittedProperties(target: Model, omit: string | Union);\n\n/**\n * Returns the model with only the given properties included.\n * @param pick List of properties to include\n */\nextern dec withPickedProperties(target: Model, pick: string | Union);\n\n//---------------------------------------------------------------------------\n// Paging\n//---------------------------------------------------------------------------\n\n/**\n * Mark this operation as a `list` operation that returns a paginated list of items.\n */\nextern dec list(target: Operation);\n\n/**\n * Pagination property defining the number of items to skip.\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n * }\n * @list op listPets(@offset skip: int32, @pageSize pageSize: int8): Page<Pet>;\n * ```\n */\nextern dec offset(target: ModelProperty);\n\n/**\n * Pagination property defining the page index.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n * }\n * @list op listPets(@pageIndex page: int32, @pageSize pageSize: int8): Page<Pet>;\n * ```\n */\nextern dec pageIndex(target: ModelProperty);\n\n/**\n * Specify the pagination parameter that controls the maximum number of items to include in a page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n * }\n * @list op listPets(@pageIndex page: int32, @pageSize pageSize: int8): Page<Pet>;\n * ```\n */\nextern dec pageSize(target: ModelProperty);\n\n/**\n * Specify the the property that contains the array of page items.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n * }\n * @list op listPets(@pageIndex page: int32, @pageSize pageSize: int8): Page<Pet>;\n * ```\n */\nextern dec pageItems(target: ModelProperty);\n\n/**\n * Pagination property defining the token to get to the next page.\n * It MUST be specified both on the request parameter and the response.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @continuationToken continuationToken: string;\n * }\n * @list op listPets(@continuationToken continuationToken: string): Page<Pet>;\n * ```\n */\nextern dec continuationToken(target: ModelProperty);\n\n/**\n * Pagination property defining a link to the next page.\n *\n * It is expected that navigating to the link will return the same set of responses as the operation that returned the current page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @nextLink next: url;\n *   @prevLink prev: url;\n *   @firstLink first: url;\n *   @lastLink last: url;\n * }\n * @list op listPets(): Page<Pet>;\n * ```\n */\nextern dec nextLink(target: ModelProperty);\n\n/**\n * Pagination property defining a link to the previous page.\n *\n * It is expected that navigating to the link will return the same set of responses as the operation that returned the current page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @nextLink next: url;\n *   @prevLink prev: url;\n *   @firstLink first: url;\n *   @lastLink last: url;\n * }\n * @list op listPets(): Page<Pet>;\n * ```\n */\nextern dec prevLink(target: ModelProperty);\n\n/**\n * Pagination property defining a link to the first page.\n *\n * It is expected that navigating to the link will return the same set of responses as the operation that returned the current page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @nextLink next: url;\n *   @prevLink prev: url;\n *   @firstLink first: url;\n *   @lastLink last: url;\n * }\n * @list op listPets(): Page<Pet>;\n * ```\n */\nextern dec firstLink(target: ModelProperty);\n\n/**\n * Pagination property defining a link to the last page.\n *\n * It is expected that navigating to the link will return the same set of responses as the operation that returned the current page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @nextLink next: url;\n *   @prevLink prev: url;\n *   @firstLink first: url;\n *   @lastLink last: url;\n * }\n * @list op listPets(): Page<Pet>;\n * ```\n */\nextern dec lastLink(target: ModelProperty);\n\n//---------------------------------------------------------------------------\n// Debugging\n//---------------------------------------------------------------------------\n\n/**\n * A debugging decorator used to inspect a type.\n * @param text Custom text to log\n */\nextern dec inspectType(target: unknown, text: valueof string);\n\n/**\n * A debugging decorator used to inspect a type name.\n * @param text Custom text to log\n */\nextern dec inspectTypeName(target: unknown, text: valueof string);\n",
  "../compiler/lib/std/reflection.tsp": "namespace TypeSpec.Reflection;\n\nmodel Enum {}\nmodel EnumMember {}\nmodel Interface {}\nmodel Model {}\nmodel ModelProperty {}\nmodel Namespace {}\nmodel Operation {}\nmodel Scalar {}\nmodel Union {}\nmodel UnionVariant {}\nmodel StringTemplate {}\n",
  "../compiler/lib/std/projected-names.tsp": "// Set of projections consuming the @projectedName decorator\n#suppress \"projections-are-experimental\"\nprojection op#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n  }\n}\n\n#suppress \"projections-are-experimental\"\nprojection interface#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n  }\n}\n\n#suppress \"projections-are-experimental\"\nprojection model#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n\n    self::properties::forEach((p) => {\n      if hasProjectedName(p, targetName) {\n        self::renameProperty(p::name, getProjectedName(p, targetName));\n      };\n    });\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n\n    self::projectionBase::properties::forEach((p) => {\n      if hasProjectedName(p, targetName) {\n        self::renameProperty(getProjectedName(p, targetName), p::name);\n      };\n    });\n  }\n}\n\n#suppress \"projections-are-experimental\"\nprojection enum#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n\n    self::members::forEach((p) => {\n      if hasProjectedName(p, targetName) {\n        self::renameMember(p::name, getProjectedName(p, targetName));\n      };\n    });\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n\n    self::projectionBase::members::forEach((p) => {\n      if hasProjectedName(p, targetName) {\n        self::renameMember(getProjectedName(p, targetName), p::name);\n      };\n    });\n  }\n}\n\n#suppress \"projections-are-experimental\"\nprojection union#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n  }\n}\n",
  "../compiler/lib/std/visibility.tsp": "// Copyright (c) Microsoft Corporation\n// Licensed under the MIT license.\n\nimport \"../../dist/src/lib/tsp-index.js\";\n\nusing TypeSpec.Reflection;\n\nnamespace TypeSpec;\n\n/**\n * Indicates that a property is only considered to be present or applicable (\"visible\") with\n * the in the given named contexts (\"visibilities\"). When a property has no visibilities applied\n * to it, it is implicitly visible always.\n *\n * As far as the TypeSpec core library is concerned, visibilities are open-ended and can be arbitrary\n * strings, but  the following visibilities are well-known to standard libraries and should be used\n * with standard emitters that interpret them as follows:\n *\n * - \"read\": output of any operation.\n * - \"create\": input to operations that create an entity..\n * - \"query\": input to operations that read data.\n * - \"update\": input to operations that update data.\n * - \"delete\": input to operations that delete data.\n *\n * See also: [Automatic visibility](https://typespec.io/docs/libraries/http/operations#automatic-visibility)\n *\n * @param visibilities List of visibilities which apply to this property.\n *\n * @example\n *\n * ```typespec\n * model Dog {\n *   // the service will generate an ID, so you don't need to send it.\n *   @visibility(Lifecycle.Read) id: int32;\n *   // the service will store this secret name, but won't ever return it\n *   @visibility(Lifecycle.Create, Lifecycle.Update) secretName: string;\n *   // the regular name is always present\n *   name: string;\n * }\n * ```\n */\nextern dec visibility(target: ModelProperty, ...visibilities: valueof (string | EnumMember)[]);\n\n/**\n * Indicates that a property is not visible in the given visibility class.\n *\n * This decorator removes all active visibility modifiers from the property within\n * the given visibility class.\n *\n * @param visibilityClass The visibility class to make the property invisible within.\n *\n * @example\n * ```typespec\n * model Example {\n *   @invisible(Lifecycle)\n *   hidden_property: string;\n * }\n * ```\n */\nextern dec invisible(target: ModelProperty, visibilityClass: Enum);\n\n/**\n * Removes visibility modifiers from a property.\n *\n * If the visibility modifiers for a visibility class have not been initialized,\n * this decorator will use the default visibility modifiers for the visibility\n * class as the default modifier set.\n *\n * @param target The property to remove visibility from.\n * @param visibilities The visibility modifiers to remove from the target property.\n *\n * @example\n * ```typespec\n * model Example {\n *   // This property will have the Create and Update visibilities, but not the\n *   // Read visibility, since it is removed.\n *   @removeVisibility(Lifecycle.Read)\n *   secret_property: string;\n * }\n * ```\n */\nextern dec removeVisibility(target: ModelProperty, ...visibilities: valueof EnumMember[]);\n\n/**\n * Removes properties that are not considered to be present or applicable\n * (\"visible\") in the given named contexts (\"visibilities\"). Can be used\n * together with spread to effectively spread only visible properties into\n * a new model.\n *\n * See also: [Automatic visibility](https://typespec.io/docs/libraries/http/operations#automatic-visibility)\n *\n * When using an emitter that applies visibility automatically, it is generally\n * not necessary to use this decorator.\n *\n * @param visibilities List of visibilities which apply to this property.\n *\n * @example\n * ```typespec\n * model Dog {\n *   @visibility(\"read\") id: int32;\n *   @visibility(\"create\", \"update\") secretName: string;\n *   name: string;\n * }\n *\n * // The spread operator will copy all the properties of Dog into DogRead,\n * // and @withVisibility will then remove those that are not visible with\n * // create or update visibility.\n * //\n * // In this case, the id property is removed, and the name and secretName\n * // properties are kept.\n * @withVisibility(\"create\", \"update\")\n * model DogCreateOrUpdate {\n *   ...Dog;\n * }\n *\n * // In this case the id and name properties are kept and the secretName property\n * // is removed.\n * @withVisibility(\"read\")\n * model DogRead {\n *   ...Dog;\n * }\n * ```\n */\nextern dec withVisibility(target: Model, ...visibilities: valueof (string | EnumMember)[]);\n\n/**\n * Set the visibility of key properties in a model if not already set.\n *\n * This will set the visibility modifiers of all key properties in the model if the visibility is not already _explicitly_ set,\n * but will not change the visibility of any properties that have visibility set _explicitly_, even if the visibility\n * is the same as the default visibility.\n *\n * Visibility may be explicitly set using any of the following decorators:\n *\n * - `@visibility`\n * - `@removeVisibility`\n * - `@invisible`\n *\n * @param visibility The desired default visibility value. If a key property already has visibility set, it will not be changed.\n */\nextern dec withDefaultKeyVisibility(target: Model, visibility: valueof string | EnumMember);\n\n/**\n * Sets which visibilities apply to parameters for the given operation.\n *\n * @param visibilities List of visibility strings which apply to this operation.\n */\nextern dec parameterVisibility(target: Operation, ...visibilities: valueof (string | EnumMember)[]);\n\n/**\n * Sets which visibilities apply to the return type for the given operation.\n * @param visibilities List of visibility strings which apply to this operation.\n */\nextern dec returnTypeVisibility(\n  target: Operation,\n  ...visibilities: valueof (string | EnumMember)[]\n);\n\n/**\n * Returns the model with non-updateable properties removed.\n */\nextern dec withUpdateableProperties(target: Model);\n\n/**\n * Declares the default visibility modifiers for a visibility class.\n *\n * The default modifiers are used when a property does not have any visibility decorators\n * applied to it.\n *\n * The modifiers passed to this decorator _MUST_ be members of the target Enum.\n *\n * @param visibilities the list of modifiers to use as the default visibility modifiers.\n */\nextern dec defaultVisibility(target: Enum, ...visibilities: valueof EnumMember[]);\n\n/**\n * A visibility class for resource lifecycle phases.\n *\n * These visibilities control whether a property is visible during the create, read, and update phases of a resource's\n * lifecycle.\n *\n * @example\n * ```typespec\n * model Dog {\n *  @visibility(Lifecycle.Read) id: int32;\n *  @visibility(Lifecycle.Create, Lifecycle.Update) secretName: string;\n *  name: string;\n * }\n * ```\n *\n * In this example, the `id` property is only visible during the read phase, and the `secretName` property is only visible\n * during the create and update phases. This means that the server will return the `id` property when returning a `Dog`,\n * but the client will not be able to set or update it. In contrast, the `secretName` property can be set when creating\n * or updating a `Dog`, but the server will never return it. The `name` property has no visibility modifiers and is\n * therefore visible in all phases.\n */\nenum Lifecycle {\n  Create,\n  Read,\n  Update,\n}\n\n/**\n * A visibility filter, used to specify which properties should be included when\n * using the `withVisibilityFilter` decorator.\n *\n * The filter matches any property with ALL of the following:\n * - If the `any` key is present, the property must have at least one of the specified visibilities.\n * - If the `all` key is present, the property must have all of the specified visibilities.\n * - If the `none` key is present, the property must have none of the specified visibilities.\n */\nmodel VisibilityFilter {\n  any?: EnumMember[];\n  all?: EnumMember[];\n  none?: EnumMember[];\n}\n\n/**\n * Applies the given visibility filter to the properties of the target model.\n *\n * This transformation is recursive, so it will also apply the filter to any nested\n * or referenced models that are the types of any properties in the `target`.\n *\n * @param target The model to apply the visibility filter to.\n * @param filter The visibility filter to apply to the properties of the target model.\n *\n * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * @withVisibilityFilter(#{ all: #[Lifecycle.Read] })\n * model DogRead {\n *  ...Dog\n * }\n * ```\n */\nextern dec withVisibilityFilter(target: Model, filter: valueof VisibilityFilter);\n\n/**\n * Transforms the `target` model to include only properties that are visible during the\n * \"Update\" lifecycle phase.\n *\n * Any nested models of optional properties will be transformed into the \"CreateOrUpdate\"\n * lifecycle phase instead of the \"Update\" lifecycle phase, so that nested models may be\n * fully updated.\n *\n * @param target The model to apply the transformation to.\n *\n * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   @visibility(Lifecycle.Create, Lifecycle.Update)\n *   secretName: string;\n *\n *   name: string;\n * }\n *\n * @withLifecycleUpdate\n * model DogUpdate {\n *   ...Dog\n * }\n * ```\n */\nextern dec withLifecycleUpdate(target: Model);\n\n/**\n * A copy of the input model `T` with only the properties that are visible during the\n * \"Create\" resource lifecycle phase.\n *\n * This transformation is recursive, and will include only properties that have the\n * `Lifecycle.Create` visibility modifier.\n *\n * If a `NameTemplate` is provided, the new model will be named according to the template.\n * The template uses the same syntax as the `@friendlyName` decorator.\n *\n * @template T The model to transform.\n * @template NameTemplate The name template to use for the new model.\n *\n *  * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * model CreateDog is Create<Dog>;\n * ```\n */\n@friendlyName(NameTemplate, T)\n@withVisibilityFilter(#{ all: #[Lifecycle.Create] })\nmodel Create<T extends Reflection.Model, NameTemplate extends valueof string = \"Create{name}\"> {\n  ...T;\n}\n\n/**\n * A copy of the input model `T` with only the properties that are visible during the\n * \"Read\" resource lifecycle phase.\n *\n * This transformation is recursive, and will include only properties that have the\n * `Lifecycle.Read` visibility modifier.\n *\n * If a `NameTemplate` is provided, the new model will be named according to the template.\n * The template uses the same syntax as the `@friendlyName` decorator.\n *\n * @template T The model to transform.\n * @template NameTemplate The name template to use for the new model.\n *\n *  * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * model ReadDog is Read<Dog>;\n * ```\n */\n@friendlyName(NameTemplate, T)\n@withVisibilityFilter(#{ all: #[Lifecycle.Read] })\nmodel Read<T extends Reflection.Model, NameTemplate extends valueof string = \"Read{name}\"> {\n  ...T;\n}\n\n/**\n * A copy of the input model `T` with only the properties that are visible during the\n * \"Update\" resource lifecycle phase.\n *\n * This transformation will include only the properties that have the `Lifecycle.Update`\n * visibility modifier, and the types of all properties will be replaced with the\n * equivalent `CreateOrUpdate` transformation.\n *\n * If a `NameTemplate` is provided, the new model will be named according to the template.\n * The template uses the same syntax as the `@friendlyName` decorator.\n *\n * @template T The model to transform.\n * @template NameTemplate The name template to use for the new model.\n *\n *  * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * model UpdateDog is Update<Dog>;\n * ```\n */\n@friendlyName(NameTemplate, T)\n@withLifecycleUpdate\nmodel Update<T extends Reflection.Model, NameTemplate extends valueof string = \"Update{name}\"> {\n  ...T;\n}\n\n/**\n * A copy of the input model `T` with only the properties that are visible during the\n * \"Create\" or \"Update\" resource lifecycle phases.\n *\n * This transformation is recursive, and will include only properties that have the\n * `Lifecycle.Create` or `Lifecycle.Update` visibility modifier.\n *\n * If a `NameTemplate` is provided, the new model will be named according to the template.\n * The template uses the same syntax as the `@friendlyName` decorator.\n *\n * @template T The model to transform.\n * @template NameTemplate The name template to use for the new model.\n *\n *  * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * model CreateOrUpdateDog is CreateOrUpdate<Dog>;\n * ```\n */\n@friendlyName(NameTemplate, T)\n@withVisibilityFilter(#{ any: #[Lifecycle.Create, Lifecycle.Update] })\nmodel CreateOrUpdate<\n  T extends Reflection.Model,\n  NameTemplate extends valueof string = \"CreateOrUpdate{name}\"\n> {\n  ...T;\n}\n",
  "lib/http.tsp": "import \"../dist/src/tsp-index.js\";\nimport \"./decorators.tsp\";\nimport \"./private.decorators.tsp\";\nimport \"./auth.tsp\";\n\nnamespace TypeSpec.Http;\n\nusing Private;\n\n/**\n * Describes an HTTP response.\n *\n * @template Status The status code of the response.\n */\n@doc(\"\")\nmodel Response<Status> {\n  @doc(\"The status code.\")\n  @statusCode\n  statusCode: Status;\n}\n\n/**\n * Defines a model with a single property of the given type, marked with `@body`.\n *\n * This can be useful in situations where you cannot use a bare type as the body\n * and it is awkward to add a property.\n *\n * @template Type The type of the model's `body` property.\n */\n@doc(\"\")\nmodel Body<Type> {\n  @body\n  @doc(\"The body type of the operation request or response.\")\n  body: Type;\n}\n\n/**\n * The Location header contains the URL where the status of the long running operation can be checked.\n */\nmodel LocationHeader {\n  @doc(\"The Location header contains the URL where the status of the long running operation can be checked.\")\n  @header\n  location: string;\n}\n\n// Don't put @doc on these, change `getStatusCodeDescription` implementation\n// to update the default descriptions for these status codes. This ensures\n// that we get consistent emit between different ways to spell the same\n// responses in TypeSpec.\n\n/**\n * The request has succeeded.\n */\nmodel OkResponse is Response<200>;\n/**\n * The request has succeeded and a new resource has been created as a result.\n */\nmodel CreatedResponse is Response<201>;\n/**\n * The request has been accepted for processing, but processing has not yet completed.\n */\nmodel AcceptedResponse is Response<202>;\n/**\n * There is no content to send for this request, but the headers may be useful.\n */\nmodel NoContentResponse is Response<204>;\n/**\n * The URL of the requested resource has been changed permanently. The new URL is given in the response.\n */\nmodel MovedResponse is Response<301> {\n  ...LocationHeader;\n}\n/**\n * The client has made a conditional request and the resource has not been modified.\n */\nmodel NotModifiedResponse is Response<304>;\n/**\n * The server could not understand the request due to invalid syntax.\n */\nmodel BadRequestResponse is Response<400>;\n/**\n * Access is unauthorized.\n */\nmodel UnauthorizedResponse is Response<401>;\n/**\n * Access is forbidden.\n */\nmodel ForbiddenResponse is Response<403>;\n/**\n * The server cannot find the requested resource.\n */\nmodel NotFoundResponse is Response<404>;\n/**\n * The request conflicts with the current state of the server.\n */\nmodel ConflictResponse is Response<409>;\n\n/**\n * Produces a new model with the same properties as T, but with `@query`,\n * `@header`, `@body`, and `@path` decorators removed from all properties.\n *\n * @template Data The model to spread as the plain data.\n */\n@plainData\nmodel PlainData<Data> {\n  ...Data;\n}\n\n@Private.httpFile\nmodel File {\n  contentType?: string;\n  filename?: string;\n  contents: bytes;\n}\n\nmodel HttpPartOptions {\n  /** Name of the part when using the array form. */\n  name?: string;\n}\n\n@Private.httpPart(Type, Options)\nmodel HttpPart<Type, Options extends valueof HttpPartOptions = #{}> {}\n\nmodel Link {\n  target: url;\n  rel: string;\n  attributes?: Record<unknown>;\n}\n\nscalar LinkHeader<T extends Record<url> | Link[]> extends string;\n",
  "lib/decorators.tsp": "namespace TypeSpec.Http;\n\nusing TypeSpec.Reflection;\n\n/**\n * Header options.\n */\nmodel HeaderOptions {\n  /**\n   * Name of the header when sent over HTTP.\n   */\n  name?: string;\n\n  /**\n   * Determines the format of the array if type array is used.\n   */\n  format?: \"csv\" | \"multi\" | \"tsv\" | \"ssv\" | \"pipes\" | \"simple\" | \"form\";\n}\n\n/**\n * Specify this property is to be sent or received as an HTTP header.\n *\n * @param headerNameOrOptions Optional name of the header when sent over HTTP or header options.\n *  By default the header name will be the property name converted from camelCase to kebab-case. (e.g. `contentType` -> `content-type`)\n *\n * @example\n *\n * ```typespec\n * op read(@header accept: string): {@header(\"ETag\") eTag: string};\n * op create(@header({name: \"X-Color\", format: \"csv\"}) colors: string[]): void;\n * ```\n *\n * @example Implicit header name\n *\n * ```typespec\n * op read(): {@header contentType: string}; // headerName: content-type\n * op update(@header ifMatch: string): void; // headerName: if-match\n * ```\n */\nextern dec header(target: ModelProperty, headerNameOrOptions?: string | HeaderOptions);\n\n/**\n * Cookie Options.\n */\nmodel CookieOptions {\n  /**\n   * Name in the cookie.\n   */\n  name?: string;\n}\n\n/**\n * Specify this property is to be sent or received in the cookie.\n *\n * @param cookieNameOrOptions Optional name of the cookie in the cookie or cookie options.\n *  By default the cookie name will be the property name converted from camelCase to snake_case. (e.g. `authToken` -> `auth_token`)\n *\n * @example\n *\n * ```typespec\n * op read(@cookie token: string): {data: string[]};\n * op create(@cookie({name: \"auth_token\"}) data: string[]): void;\n * ```\n *\n * @example Implicit header name\n *\n * ```typespec\n * op read(): {@cookie authToken: string}; // headerName: auth_token\n * op update(@cookie AuthToken: string): void; // headerName: auth_token\n * ```\n */\nextern dec cookie(target: ModelProperty, cookieNameOrOptions?: valueof string | CookieOptions);\n\n/**\n * Query parameter options.\n */\nmodel QueryOptions {\n  /**\n   * Name of the query when included in the url.\n   */\n  name?: string;\n\n  /**\n   * If true send each value in the array/object as a separate query parameter.\n   * Equivalent of adding `*` in the path parameter as per [RFC-6570](https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.3)\n   *\n   *  | Style  | Explode | Uri Template   | Primitive value id = 5 | Array id = [3, 4, 5]    | Object id = {\"role\": \"admin\", \"firstName\": \"Alex\"} |\n   *  | ------ | ------- | -------------- | ---------------------- | ----------------------- | -------------------------------------------------- |\n   *  | simple | false   | `/users{?id}`  | `/users?id=5`          | `/users?id=3,4,5`       | `/users?id=role,admin,firstName,Alex`              |\n   *  | simple | true    | `/users{?id*}` | `/users?id=5`          | `/users?id=3&id=4&id=5` | `/users?role=admin&firstName=Alex`                 |\n   *\n   */\n  explode?: boolean;\n\n  /**\n   * Determines the format of the array if type array is used.\n   * **DEPRECATED**: use explode: true instead of `multi` or `@encode`\n   */\n  format?: \"multi\" | \"csv\" | \"ssv\" | \"tsv\" | \"simple\" | \"form\" | \"pipes\";\n}\n\n/**\n * Specify this property is to be sent as a query parameter.\n *\n * @param queryNameOrOptions Optional name of the query when included in the url or query parameter options.\n *\n * @example\n *\n * ```typespec\n * op read(@query select: string, @query(\"order-by\") orderBy: string): void;\n * op list(@query(#{name: \"id\", explode: true}) ids: string[]): void;\n * ```\n */\nextern dec query(target: ModelProperty, queryNameOrOptions?: valueof string | QueryOptions);\n\nmodel PathOptions {\n  /** Name of the parameter in the uri template. */\n  name?: string;\n\n  /**\n   * When interpolating this parameter in the case of array or object expand each value using the given style.\n   * Equivalent of adding `*` in the path parameter as per [RFC-6570](https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.3)\n   */\n  explode?: boolean;\n\n  /**\n   * Different interpolating styles for the path parameter.\n   * - `simple`: No special encoding.\n   * - `label`: Using `.` separator.\n   * - `matrix`: `;` as separator.\n   * - `fragment`: `#` as separator.\n   * - `path`: `/` as separator.\n   */\n  style?: \"simple\" | \"label\" | \"matrix\" | \"fragment\" | \"path\";\n\n  /**\n   * When interpolating this parameter do not encode reserved characters.\n   * Equivalent of adding `+` in the path parameter as per [RFC-6570](https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.3)\n   */\n  allowReserved?: boolean;\n}\n\n/**\n * Explicitly specify that this property is to be interpolated as a path parameter.\n *\n * @param paramNameOrOptions Optional name of the parameter in the uri template or options.\n *\n * @example\n *\n * ```typespec\n * @route(\"/read/{explicit}/things/{implicit}\")\n * op read(@path explicit: string, implicit: string): void;\n * ```\n */\nextern dec path(target: ModelProperty, paramNameOrOptions?: valueof string | PathOptions);\n\n/**\n * Explicitly specify that this property type will be exactly the HTTP body.\n *\n * This means that any properties under `@body` cannot be marked as headers, query parameters, or path parameters.\n * If wanting to change the resolution of the body but still mix parameters, use `@bodyRoot`.\n *\n * @example\n *\n * ```typespec\n * op upload(@body image: bytes): void;\n * op download(): {@body image: bytes};\n * ```\n */\nextern dec body(target: ModelProperty);\n\n/**\n * Specify that the body resolution should be resolved from that property.\n * By default the body is resolved by including all properties in the operation request/response that are not metadata.\n * This allows to nest the body in a property while still allowing to use headers, query parameters, and path parameters in the same model.\n *\n * @example\n *\n * ```typespec\n * op upload(@bodyRoot user: {name: string, @header id: string}): void;\n * op download(): {@bodyRoot user: {name: string, @header id: string}};\n * ```\n */\nextern dec bodyRoot(target: ModelProperty);\n/**\n * Specify that this property shouldn't be included in the HTTP body.\n * This can be useful when bundling metadata together that would result in an empty property to be included in the body.\n *\n * @example\n *\n * ```typespec\n * op upload(name: string, @bodyIgnore headers: {@header id: string}): void;\n * ```\n */\nextern dec bodyIgnore(target: ModelProperty);\n\n/**\n * @example\n *\n * ```tsp\n * op upload(\n *   @header `content-type`: \"multipart/form-data\",\n *   @multipartBody body: {\n *     fullName: HttpPart<string>,\n *     headShots: HttpPart<Image>[]\n *   }\n * ): void;\n * ```\n */\nextern dec multipartBody(target: ModelProperty);\n\n/**\n * Specify the status code for this response. Property type must be a status code integer or a union of status code integer.\n *\n * @example\n *\n * ```typespec\n * op read(): {\n *   @statusCode _: 200;\n *   @body pet: Pet;\n * };\n * op create(): {\n *   @statusCode _: 201 | 202;\n * };\n * ```\n */\nextern dec statusCode(target: ModelProperty);\n\n/**\n * Specify the HTTP verb for the target operation to be `GET`.\n *\n * @example\n *\n * ```typespec\n * @get op read(): string\n * ```\n */\nextern dec get(target: Operation);\n\n/**\n * Specify the HTTP verb for the target operation to be `PUT`.\n *\n * @example\n *\n * ```typespec\n * @put op set(pet: Pet): void\n * ```\n */\nextern dec put(target: Operation);\n\n/**\n * Specify the HTTP verb for the target operation to be `POST`.\n *\n * @example\n *\n * ```typespec\n * @post op create(pet: Pet): void\n * ```\n */\nextern dec post(target: Operation);\n\n/**\n * Specify the HTTP verb for the target operation to be `PATCH`.\n *\n * @example\n *\n * ```typespec\n * @patch op update(pet: Pet): void\n * ```\n */\nextern dec patch(target: Operation);\n\n/**\n * Specify the HTTP verb for the target operation to be `DELETE`.\n *\n * @example\n *\n * ```typespec\n * @delete op set(petId: string): void\n * ```\n */\nextern dec delete(target: Operation);\n\n/**\n * Specify the HTTP verb for the target operation to be `HEAD`.\n * @example\n *\n * ```typespec\n * @head op ping(petId: string): void\n * ```\n */\nextern dec head(target: Operation);\n\n/**\n * Specify an endpoint for this service. Multiple `@server` decorators can be used to specify multiple endpoints.\n *\n *  @param url Server endpoint\n *  @param description Description of the endpoint\n *  @param parameters Optional set of parameters used to interpolate the url.\n *\n * @example\n *\n * ```typespec\n * @service\n * @server(\"https://example.com\")\n * namespace PetStore;\n * ```\n *\n * @example With a description\n *\n * ```typespec\n * @service\n * @server(\"https://example.com\", \"Single server endpoint\")\n * namespace PetStore;\n * ```\n *\n * @example Parameterized\n *\n * ```typespec\n * @server(\"https://{region}.foo.com\", \"Regional endpoint\", {\n *   @doc(\"Region name\")\n *   region?: string = \"westus\",\n * })\n * ```\n *\n * @example Multiple\n * ```typespec\n * @service\n * @server(\"https://example.com\", \"Standard endpoint\")\n * @server(\"https://{project}.private.example.com\", \"Private project endpoint\", {\n *   project: string;\n * })\n * namespace PetStore;\n * ```\n *\n */\nextern dec server(\n  target: Namespace,\n  url: valueof string,\n  description?: valueof string,\n  parameters?: Record<unknown>\n);\n\n/**\n * Specify authentication for a whole service or specific methods. See the [documentation in the Http library](https://typespec.io/docs/libraries/http/authentication) for full details.\n *\n * @param auth Authentication configuration. Can be a single security scheme, a union(either option is valid authentication) or a tuple (must use all authentication together)\n * @example\n *\n * ```typespec\n * @service\n * @useAuth(BasicAuth)\n * namespace PetStore;\n * ```\n */\nextern dec useAuth(target: Namespace | Interface | Operation, auth: {} | Union | {}[]);\n\n/**\n * Specify if inapplicable metadata should be included in the payload for the given entity.\n * @param value If true, inapplicable metadata will be included in the payload.\n */\nextern dec includeInapplicableMetadataInPayload(target: unknown, value: valueof boolean);\n\n/**\n * Defines the relative route URI template for the target operation as defined by [RFC 6570](https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.3)\n *\n * `@route` can only be applied to operations, namespaces, and interfaces.\n *\n * @param uriTemplate Uri template for this operation.\n * @param options _DEPRECATED_ Set of parameters used to configure the route. Supports `{shared: true}` which indicates that the route may be shared by several operations.\n *\n * @example Simple path parameter\n *\n * ```typespec\n * @route(\"/widgets/{id}\") op getWidget(@path id: string): Widget;\n * ```\n *\n * @example Reserved characters\n * ```typespec\n * @route(\"/files{+path}\") op getFile(@path path: string): bytes;\n * ```\n *\n * @example Query parameter\n * ```typespec\n * @route(\"/files\") op list(select?: string, filter?: string): Files[];\n * @route(\"/files{?select,filter}\") op listFullUriTemplate(select?: string, filter?: string): Files[];\n * ```\n */\nextern dec route(\n  target: Namespace | Interface | Operation,\n  path: valueof string,\n  options?: {\n    shared?: boolean,\n  }\n);\n\n/**\n * `@sharedRoute` marks the operation as sharing a route path with other operations.\n *\n * When an operation is marked with `@sharedRoute`, it enables other operations to share the same\n * route path as long as those operations are also marked with `@sharedRoute`.\n *\n * `@sharedRoute` can only be applied directly to operations.\n *\n * ```typespec\n * @sharedRoute\n * @route(\"/widgets\")\n * op getWidget(@path id: string): Widget;\n * ```\n */\nextern dec sharedRoute(target: Operation);\n",
  "lib/private.decorators.tsp": "import \"../dist/src/private.decorators.js\";\n\n/**\n * Private decorators. Those are meant for internal use inside Http types only.\n */\nnamespace TypeSpec.Http.Private;\n\nextern dec plainData(target: TypeSpec.Reflection.Model);\nextern dec httpFile(target: TypeSpec.Reflection.Model);\nextern dec httpPart(\n  target: TypeSpec.Reflection.Model,\n  type: unknown,\n  options: valueof HttpPartOptions\n);\n",
  "lib/auth.tsp": "namespace TypeSpec.Http;\n\n@doc(\"Authentication type\")\nenum AuthType {\n  @doc(\"HTTP\")\n  http,\n\n  @doc(\"API key\")\n  apiKey,\n\n  @doc(\"OAuth2\")\n  oauth2,\n\n  @doc(\"OpenID connect\")\n  openIdConnect,\n\n  @doc(\"Empty auth\")\n  noAuth,\n}\n\n/**\n * Basic authentication is a simple authentication scheme built into the HTTP protocol.\n * The client sends HTTP requests with the Authorization header that contains the word Basic word followed by a space and a base64-encoded string username:password.\n * For example, to authorize as demo / `p@55w0rd` the client would send\n * ```\n * Authorization: Basic ZGVtbzpwQDU1dzByZA==\n * ```\n */\n@doc(\"\")\nmodel BasicAuth {\n  @doc(\"Http authentication\")\n  type: AuthType.http;\n\n  @doc(\"basic auth scheme\")\n  scheme: \"basic\";\n}\n\n/**\n * Bearer authentication (also called token authentication) is an HTTP authentication scheme that involves security tokens called bearer tokens.\n * The name “Bearer authentication” can be understood as “give access to the bearer of this token.” The bearer token is a cryptic string, usually generated by the server in response to a login request.\n * The client must send this token in the Authorization header when making requests to protected resources:\n * ```\n * Authorization: Bearer <token>\n * ```\n */\n@doc(\"\")\nmodel BearerAuth {\n  @doc(\"Http authentication\")\n  type: AuthType.http;\n\n  @doc(\"bearer auth scheme\")\n  scheme: \"bearer\";\n}\n\n@doc(\"Describes the location of the API key\")\nenum ApiKeyLocation {\n  @doc(\"API key is a header value\")\n  header,\n\n  @doc(\"API key is a query parameter\")\n  query,\n\n  @doc(\"API key is found in a cookie\")\n  cookie,\n}\n\n/**\n * An API key is a token that a client provides when making API calls. The key can be sent in the query string:\n *\n * ```\n * GET /something?api_key=abcdef12345\n * ```\n *\n * or as a request header\n *\n * ```\n * GET /something HTTP/1.1\n * X-API-Key: abcdef12345\n * ```\n *\n * or as a cookie\n *\n * ```\n * GET /something HTTP/1.1\n * Cookie: X-API-KEY=abcdef12345\n * ```\n *\n * @template Location The location of the API key\n * @template Name The name of the API key\n */\n@doc(\"\")\nmodel ApiKeyAuth<Location extends ApiKeyLocation, Name extends string> {\n  @doc(\"API key authentication\")\n  type: AuthType.apiKey;\n\n  @doc(\"location of the API key\")\n  in: Location;\n\n  @doc(\"name of the API key\")\n  name: Name;\n}\n\n/**\n * OAuth 2.0 is an authorization protocol that gives an API client limited access to user data on a web server.\n *\n * OAuth relies on authentication scenarios called flows, which allow the resource owner (user) to share the protected content from the resource server without sharing their credentials.\n * For that purpose, an OAuth 2.0 server issues access tokens that the client applications can use to access protected resources on behalf of the resource owner.\n * For more information about OAuth 2.0, see oauth.net and RFC 6749.\n *\n * @template Flows The list of supported OAuth2 flows\n * @template Scopes The list of OAuth2 scopes, which are common for every flow from `Flows`. This list is combined with the scopes defined in specific OAuth2 flows.\n */\n@doc(\"\")\nmodel OAuth2Auth<Flows extends OAuth2Flow[], Scopes extends string[] = []> {\n  @doc(\"OAuth2 authentication\")\n  type: AuthType.oauth2;\n\n  @doc(\"Supported OAuth2 flows\")\n  flows: Flows;\n\n  @doc(\"Oauth2 scopes of every flow. Overridden by scope definitions in specific flows\")\n  defaultScopes: Scopes;\n}\n\n@doc(\"Describes the OAuth2 flow type\")\nenum OAuth2FlowType {\n  @doc(\"authorization code flow\")\n  authorizationCode,\n\n  @doc(\"implicit flow\")\n  implicit,\n\n  @doc(\"password flow\")\n  password,\n\n  @doc(\"client credential flow\")\n  clientCredentials,\n}\n\nalias OAuth2Flow = AuthorizationCodeFlow | ImplicitFlow | PasswordFlow | ClientCredentialsFlow;\n\n@doc(\"Authorization Code flow\")\nmodel AuthorizationCodeFlow {\n  @doc(\"authorization code flow\")\n  type: OAuth2FlowType.authorizationCode;\n\n  @doc(\"the authorization URL\")\n  authorizationUrl: string;\n\n  @doc(\"the token URL\")\n  tokenUrl: string;\n\n  @doc(\"the refresh URL\")\n  refreshUrl?: string;\n\n  @doc(\"list of scopes for the credential\")\n  scopes?: string[];\n}\n\n@doc(\"Implicit flow\")\nmodel ImplicitFlow {\n  @doc(\"implicit flow\")\n  type: OAuth2FlowType.implicit;\n\n  @doc(\"the authorization URL\")\n  authorizationUrl: string;\n\n  @doc(\"the refresh URL\")\n  refreshUrl?: string;\n\n  @doc(\"list of scopes for the credential\")\n  scopes?: string[];\n}\n\n@doc(\"Resource Owner Password flow\")\nmodel PasswordFlow {\n  @doc(\"password flow\")\n  type: OAuth2FlowType.password;\n\n  @doc(\"the token URL\")\n  tokenUrl: string;\n\n  @doc(\"the refresh URL\")\n  refreshUrl?: string;\n\n  @doc(\"list of scopes for the credential\")\n  scopes?: string[];\n}\n\n@doc(\"Client credentials flow\")\nmodel ClientCredentialsFlow {\n  @doc(\"client credential flow\")\n  type: OAuth2FlowType.clientCredentials;\n\n  @doc(\"the token URL\")\n  tokenUrl: string;\n\n  @doc(\"the refresh URL\")\n  refreshUrl?: string;\n\n  @doc(\"list of scopes for the credential\")\n  scopes?: string[];\n}\n\n/**\n * OpenID Connect (OIDC) is an identity layer built on top of the OAuth 2.0 protocol and supported by some OAuth 2.0 providers, such as Google and Azure Active Directory.\n * It defines a sign-in flow that enables a client application to authenticate a user, and to obtain information (or \"claims\") about that user, such as the user name, email, and so on.\n * User identity information is encoded in a secure JSON Web Token (JWT), called ID token.\n * OpenID Connect defines a discovery mechanism, called OpenID Connect Discovery, where an OpenID server publishes its metadata at a well-known URL, typically\n *\n * ```http\n * https://server.com/.well-known/openid-configuration\n * ```\n */\nmodel OpenIdConnectAuth<ConnectUrl extends string> {\n  /** Auth type */\n  type: AuthType.openIdConnect;\n\n  /** Connect url. It can be specified relative to the server URL */\n  openIdConnectUrl: ConnectUrl;\n}\n\n/**\n * This authentication option signifies that API is not secured at all.\n * It might be useful when overriding authentication on interface of operation level.\n */\n@doc(\"\")\nmodel NoAuth {\n  type: AuthType.noAuth;\n}\n"
};
const _TypeSpecLibrary_ = {
  jsSourceFiles: TypeSpecJSSources,
  typespecSourceFiles: TypeSpecSources,
};

export { $body, $bodyIgnore, $bodyRoot, $cookie, $decorators, $delete, $get, $head, $header, $includeInapplicableMetadataInPayload, $lib, $linter, $multipartBody, $patch, $path, $post, $put, $query, $route, $server, $sharedRoute, $statusCode, $useAuth, DefaultRouteProducer, Visibility, _TypeSpecLibrary_, addQueryParamsToUriTemplate, createMetadataInfo, getAllHttpServices, getAllRoutes, getAuthentication, getAuthenticationForOperation, getContentTypes, getCookieParamOptions, getHeaderFieldName, getHeaderFieldOptions, getHttpFileModel, getHttpOperation, getHttpPart, getHttpService, getOperationParameters, getOperationVerb, getPathParamName, getPathParamOptions, getQueryParamName, getQueryParamOptions, getRequestVisibility, getResponsesForOperation, getRouteOptionsForNamespace, getRoutePath, getRouteProducer, getServers, getStatusCodeDescription, getStatusCodes, getStatusCodesWithDiagnostics, getUriTemplatePathParam, getVisibilitySuffix, includeInapplicableMetadataInPayload, includeInterfaceRoutesInNamespace, isApplicableMetadata, isApplicableMetadataOrBody, isBody, isBodyIgnore, isBodyRoot, isContentTypeHeader, isCookieParam, isHeader, isHttpFile, isMetadata, isMultipartBodyProperty, isOrExtendsHttpFile, isOverloadSameEndpoint, isPathParam, isQueryParam, isSharedRoute, isStatusCode, isVisible, joinPathSegments, listHttpOperationsIn, namespace$1 as namespace, reportIfNoRoutes, resolveAuthentication, resolvePathAndParameters, resolveRequestVisibility, setAuthentication, setRoute, setRouteOptionsForNamespace, setRouteProducer, setSharedRoute, setStatusCode, validateRouteUnique };
