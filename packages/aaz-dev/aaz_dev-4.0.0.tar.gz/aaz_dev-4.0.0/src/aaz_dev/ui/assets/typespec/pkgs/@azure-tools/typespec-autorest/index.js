import { createTypeSpecLibrary, paramMessage, getProjectedName, isGlobalNamespace, isService, ignoreDiagnostics, compilerAssert, getAllTags, getSummary, getDoc, isDeprecated, isErrorModel, isErrorType, isVoidType, isNullType, isNeverType, isArrayModelType, navigateTypesInNamespace, serializeValueAsJson, isRecordModelType, getDiscriminator, getVisibility, isTemplateDeclarationOrInstance, isStringType, getPropertyType, isNumericType, getFormat, getPattern, getMinLength, getMaxLength, getMinValue, getMaxValue, getMinItems, getMaxItems, isSecret, getKnownValues, getEncode, SyntaxKind, explainStringTemplateNotSerializable, createDiagnosticCollector, resolvePath, NoTarget, isList, getPagingOperation, resolveEncodedName, reportDeprecated, getProperty, isTemplateDeclaration, interpolatePath, getRootLength, getRelativePathFromDirectory, getDirectoryPath, joinPaths, getAnyExtensionFromPath, normalizePath, listServices, projectProgram, getService, emitFile, getNamespaceFullName } from '@typespec/compiler';
import { getClientNameOverride, shouldFlattenProperty, createTCGCContext } from '@azure-tools/typespec-client-generator-core';
import { getOperationId, resolveInfo, getExternalDocs, getOpenAPITypeName, shouldInline, getParameterKey, checkDuplicateTypeName, getExtensions, isReadonlyProperty } from '@typespec/openapi';
import { getVersionsForEnum, buildVersionProjections } from '@typespec/versioning';
import { getLroMetadata, extractLroStates, getUnionAsEnum, getAsEmbeddingVector, getArmResourceIdentifierConfig, FinalStateValue, getPagedResult } from '@azure-tools/typespec-azure-core';
import { isConditionallyFlattened, isAzureResource, isArmCommonType, getArmCommonTypeOpenAPIRef } from '@azure-tools/typespec-azure-resource-manager';
import { TwoLevelMap } from '@typespec/compiler/utils';
import { createMetadataInfo, Visibility, getHttpService, reportIfNoRoutes, getServers, resolveRequestVisibility, isContentTypeHeader, getHeaderFieldOptions, getVisibilitySuffix, getAuthentication, isSharedRoute, getStatusCodeDescription } from '@typespec/http';

const EmitterOptionsSchema = {
    type: "object",
    additionalProperties: false,
    properties: {
        "output-dir": {
            type: "string",
            nullable: true,
            deprecated: true,
            description: "Deprecated DO NOT USE. Use built-in emitter-output-dir instead",
        },
        "output-file": {
            type: "string",
            nullable: true,
            description: [
                "Name of the output file.",
                "Output file will interpolate the following values:",
                " - service-name: Name of the service if multiple",
                " - version: Version of the service if multiple",
                " - azure-resource-provider-folder: Value of the azure-resource-provider-folder option",
                " - version-status: Only enabled if azure-resource-provider-folder is set. `preview` if version contains preview, stable otherwise.",
                "",
                "Default: `{azure-resource-provider-folder}/{service-name}/{version-status}/{version}/openapi.json`",
                "",
                "",
                "Example: Single service no versioning",
                " - `openapi.yaml`",
                "",
                "Example: Multiple services no versioning",
                " - `openapi.Org1.Service1.yaml`",
                " - `openapi.Org1.Service2.yaml`",
                "",
                "Example: Single service with versioning",
                " - `openapi.v1.yaml`",
                " - `openapi.v2.yaml`",
                "",
                "Example: Multiple service with versioning",
                " - `openapi.Org1.Service1.v1.yaml`",
                " - `openapi.Org1.Service1.v2.yaml`",
                " - `openapi.Org1.Service2.v1.0.yaml`",
                " - `openapi.Org1.Service2.v1.1.yaml`",
                "",
                "Example: azureResourceProviderFolder is provided",
                " - `arm-folder/AzureService/preview/2020-01-01.yaml`",
                " - `arm-folder/AzureService/preview/2020-01-01.yaml`",
            ].join("\n"),
        },
        "examples-dir": {
            type: "string",
            nullable: true,
            description: "Directory where the examples are located. Default: `{project-root}/examples`.",
            format: "absolute-path",
        },
        "examples-directory": {
            type: "string",
            nullable: true,
            deprecated: true,
            description: "DEPRECATED. Use examples-dir instead",
        },
        version: { type: "string", nullable: true },
        "azure-resource-provider-folder": { type: "string", nullable: true },
        "arm-types-dir": {
            type: "string",
            nullable: true,
            description: "Path to the common-types.json file folder. Default: '${project-root}/../../common-types/resource-management'",
        },
        "new-line": {
            type: "string",
            enum: ["crlf", "lf"],
            nullable: true,
            default: "lf",
            description: "Set the newline character for emitting files.",
        },
        "omit-unreachable-types": {
            type: "boolean",
            nullable: true,
            description: "Omit unreachable types. By default all types declared under the service namespace will be included. With this flag on only types references in an operation will be emitted.",
        },
        "version-enum-strategy": {
            type: "string",
            nullable: true,
            description: "Decide how to deal with the Version enum when when `omit-unreachable-types` is not set. Default to 'omit'",
            default: "omit",
        },
        "include-x-typespec-name": {
            type: "string",
            enum: ["inline-only", "never"],
            nullable: true,
            default: "never",
            description: "If the generated openapi types should have the `x-typespec-name` extension set with the name of the TypeSpec type that created it.\nThis extension is meant for debugging and should not be depended on.",
        },
        "use-read-only-status-schema": {
            type: "boolean",
            nullable: true,
            default: false,
            description: "Create read-only property schema for lro status",
        },
        "emit-lro-options": {
            type: "string",
            enum: ["none", "final-state-only", "all"],
            nullable: true,
            default: "final-state-only",
            description: "Determine whether and how to emit x-ms-long-running-operation-options for lro resolution",
        },
        "arm-resource-flattening": {
            type: "boolean",
            nullable: true,
            default: false,
            description: "Back-compat flag. If true, continue to emit `x-ms-client-flatten` in for some of the ARM resource properties.",
        },
        "emit-common-types-schema": {
            type: "string",
            enum: ["never", "for-visibility-changes"],
            nullable: true,
            default: "for-visibility-changes",
            description: "Determine whether and how to emit schemas for common-types rather than referencing them",
        },
    },
    required: [],
};
const $lib = createTypeSpecLibrary({
    name: "@azure-tools/typespec-autorest",
    diagnostics: {
        "duplicate-body-types": {
            severity: "error",
            messages: {
                default: "Request has multiple body types",
            },
        },
        "duplicate-header": {
            severity: "error",
            messages: {
                default: paramMessage `The header ${"header"} is defined across multiple content types`,
            },
        },
        "duplicate-example": {
            severity: "error",
            messages: {
                default: "Duplicate @example declarations on operation",
            },
        },
        "duplicate-example-file": {
            severity: "error",
            messages: {
                default: paramMessage `Example file ${"filename"} uses duplicate title '${"title"}' for operationId '${"operationId"}'`,
            },
        },
        "invalid-schema": {
            severity: "error",
            messages: {
                default: paramMessage `Couldn't get schema for type ${"type"}`,
            },
        },
        "union-null": {
            severity: "error",
            messages: {
                default: "Cannot have a union containing only null types.",
            },
        },
        "union-unsupported": {
            severity: "warning",
            messages: {
                default: "Unions cannot be emitted to OpenAPI v2 unless all options are literals of the same type.",
                empty: "Empty unions are not supported for OpenAPI v2 - enums must have at least one value.",
            },
        },
        "invalid-multi-collection-format": {
            severity: "error",
            messages: {
                default: "The 'multi' should be applied to parameter in 'query', 'header' or 'formData'.",
            },
        },
        "inline-cycle": {
            severity: "error",
            messages: {
                default: paramMessage `Cycle detected in '${"type"}'. Use @friendlyName decorator to assign an OpenAPI definition name and make it non-inline.`,
            },
        },
        "nonspecific-scalar": {
            severity: "warning",
            messages: {
                default: paramMessage `Scalar type '${"type"}' is not specific enough. The more specific type '${"chosenType"}' has been chosen.`,
            },
        },
        "example-loading": {
            severity: "warning",
            messages: {
                default: paramMessage `Skipped loading invalid example file: ${"filename"}. Error: ${"error"}`,
                noDirectory: paramMessage `Skipping example loading from ${"directory"} because there was an error reading the directory.`,
                noOperationId: paramMessage `Skipping example file ${"filename"} because it does not contain an operationId and/or title.`,
            },
        },
        "unsupported-http-auth-scheme": {
            severity: "warning",
            messages: {
                default: paramMessage `The specified HTTP authentication scheme is not supported by this emitter: ${"scheme"}.`,
            },
        },
        "unsupported-status-code-range": {
            severity: "error",
            messages: {
                default: paramMessage `Status code range '${"start"} to '${"end"}' is not supported. OpenAPI 2.0 can only represent range 1XX, 2XX, 3XX, 4XX and 5XX. Example: \`@minValue(400) @maxValue(499)\` for 4XX.`,
            },
        },
        "unsupported-multipart-type": {
            severity: "warning",
            messages: {
                default: paramMessage `Multipart parts can only be represented as primitive types in swagger 2.0. Information is lost for part '${"part"}'.`,
            },
        },
        "unsupported-param-type": {
            severity: "warning",
            messages: {
                default: paramMessage `Parameter can only be represented as primitive types in swagger 2.0. Information is lost for part '${"part"}'.`,
            },
        },
        "cookies-unsupported": {
            severity: "warning",
            messages: {
                default: `Cookies are not supported in Swagger 2.0. Parameter was ignored.`,
            },
        },
        "invalid-format": {
            severity: "warning",
            messages: {
                default: paramMessage `'${"schema"}' format '${"format"}' is not supported in Autorest. It will not be emitted.`,
            },
        },
        "unsupported-auth": {
            severity: "warning",
            messages: {
                default: paramMessage `Authentication "${"authType"}" is not a known authentication by the openapi3 emitter, it will be ignored.`,
            },
        },
        "no-matching-version-found": {
            severity: "error",
            messages: {
                default: "The emitter did not emit any files because the specified version option does not match any versions of the service.",
            },
        },
    },
    emitter: {
        options: EmitterOptionsSchema,
    },
    state: {
        example: { description: "State for the @example decorator" },
        useRef: { description: "State for the @useRef decorator" },
    },
});
const { reportDiagnostic, createDiagnostic, stateKeys: AutorestStateKeys, getTracer } = $lib;

const namespace = "Autorest";
/**
 * `@example` - attaches example files to an operation. Multiple examples can be specified.
 *
 * @param {string} pathOrUri - path or Uri to the example file.
 * @param {string} title - name or description of the example file.
 *
 * `@example` can be specified on Operations.
 */
const $example = (context, entity, pathOrUri, title) => {
    const { program } = context;
    if (!program.stateMap(AutorestStateKeys.example).has(entity)) {
        program.stateMap(AutorestStateKeys.example).set(entity, []);
    }
    else if (program
        .stateMap(AutorestStateKeys.example)
        .get(entity)
        .find((e) => e.title === title || e.pathOrUri === pathOrUri)) {
        reportDiagnostic(program, {
            code: "duplicate-example",
            target: entity,
        });
    }
    program.stateMap(AutorestStateKeys.example).get(entity).push({
        pathOrUri,
        title,
    });
};
function getExamples(program, entity) {
    return program.stateMap(AutorestStateKeys.example).get(entity);
}
/**
 * `@useRef` - is used to replace the TypeSpec model type in emitter output with a pre-existing named OpenAPI schema such as ARM common types.
 *
 * @param {string} jsonRef - path or Uri to an OpenAPI schema.
 *
 * `@useRef` can be specified on Models and ModelProperty.
 */
const $useRef = (context, entity, jsonRef) => {
    context.program.stateMap(AutorestStateKeys.useRef).set(entity, jsonRef);
};
function getRef(program, entity) {
    const refOrProducer = program.stateMap(AutorestStateKeys.useRef).get(entity);
    return refOrProducer;
}

let AutorestOpenAPISchema;
try {
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    AutorestOpenAPISchema = (await import('./schema-BnqP8Ssi.js')).default;
}
catch {
    const name = "../schema/dist/schema.js";
    AutorestOpenAPISchema = (await import(/* @vite-ignore */ name)).default;
}

function sortWithJsonSchema(value, jsonSchema, ref) {
    const schema = jsonSchema;
    return internalSort(value, schema, new JsonSchemaReader(jsonSchema));
}
function internalSort(value, relativeSchema, reader) {
    if (typeof value !== "object" || value === null) {
        return value;
    }
    const resolvedRelativeSchema = relativeSchema && resolveSchema(relativeSchema, reader);
    if (Array.isArray(value)) {
        const itemsSchema = resolvedRelativeSchema?.type === "array" ? resolvedRelativeSchema.items : undefined;
        return value.map((x) => internalSort(x, itemsSchema, reader));
    }
    const objectSchema = resolvedRelativeSchema;
    const properties = objectSchema?.properties && Object.keys(objectSchema.properties);
    const keys = Object.keys(value);
    const ordering = objectSchema?.["x-ordering"];
    if (ordering === "url") {
        keys.sort(compareUrl);
    }
    else if (ordering !== "keep") {
        keys.sort((a, b) => {
            if (properties) {
                const aIndex = properties.indexOf(a);
                const bIndex = properties.indexOf(b);
                if (aIndex !== -1 && bIndex !== -1) {
                    return aIndex - bIndex;
                }
                else if (aIndex !== -1) {
                    return -1;
                }
                else if (bIndex !== -1) {
                    return 1;
                }
            }
            return defaultCompare(a, b);
        });
    }
    return keys.reduce((o, key) => {
        const v = value[key];
        const propertySchema = objectSchema?.properties?.[key] ??
            resolvePatternProperties(key, objectSchema?.patternProperties) ??
            resolveAdditionalProperties(objectSchema?.additionalProperties);
        if (propertySchema !== undefined) {
            o[key] = internalSort(v, propertySchema, reader);
        }
        else {
            o[key] = v;
        }
        return o;
    }, {});
}
/**
 * Default sort implementation for deterministic sorting.
 */
function defaultCompare(a, b) {
    return +(a > b) || -(b > a);
}
/** Sort urls in a specific way so path with field show up before a fixed segment. */
function compareUrl(leftPath, rightPath) {
    const leftParts = leftPath.split("/").slice(1);
    const rightParts = rightPath.split("/").slice(1);
    for (let i = 0; i < Math.max(leftParts.length, rightParts.length); i++) {
        // Have we exhausted the path parts of one of them?
        if (i === leftParts.length)
            return -1;
        if (i === rightParts.length)
            return 1;
        // Does this segment represent a path parameter (field) on either side?
        const leftIsField = leftParts[i][0] === "{";
        const rightIsField = rightParts[i][0] === "{";
        // If both are fields, try the next part regardless of the field name
        // since the field ordering is all that really matters
        if (leftIsField && rightIsField) {
            continue;
        }
        // If only one is a field, it automatically wins
        if (leftIsField || rightIsField) {
            return leftIsField ? -1 : 1;
        }
        // Sort lexicographically
        const result = defaultCompare(leftParts[i], rightParts[i]);
        if (result !== 0) {
            return result;
        }
    }
    // Must be the same
    return 0;
}
function resolveSchema(schema, reader) {
    if ("$ref" in schema) {
        return reader.resolveRef(schema.$ref);
    }
    else {
        return schema;
    }
}
function resolveJsonRef(ref, baseSchema) {
    const [file, path] = ref.split("#");
    if (file !== "") {
        throw new Error(`JsonSchemaSorter: Not supporting cross file ref: "${ref}".`);
    }
    const segments = path.split("/");
    let current = baseSchema;
    for (const segment of segments.slice(1)) {
        if (segment in current) {
            current = current[segment];
        }
        else {
            throw new Error(`JsonSchemaSorter: ref "${ref}" is invalid`);
        }
    }
    return current;
}
function resolvePatternProperties(key, patternProperties) {
    if (patternProperties === undefined) {
        return undefined;
    }
    for (const [pattern, schema] of Object.entries(patternProperties)) {
        if (key.match(pattern)) {
            return schema;
        }
    }
    return undefined;
}
function resolveAdditionalProperties(additionalProperties) {
    if (typeof additionalProperties === "boolean") {
        return undefined;
    }
    return additionalProperties;
}
class JsonSchemaReader {
    #doc;
    #defs = new Map();
    constructor(doc) {
        this.#doc = doc;
        if (doc.$defs) {
            for (const value of Object.values(doc.$defs)) {
                if ("$id" in value && value.$id) {
                    this.#defs.set(value.$id, value);
                }
            }
        }
    }
    resolveRef(ref) {
        if (ref.includes("#")) {
            return resolveJsonRef(ref, this.#doc);
        }
        else {
            const schema = this.#defs.get(ref);
            if (schema === undefined) {
                throw new Error(`JsonSchemaSorter: Cannot find schema with $id ${ref}`);
            }
            if ("$ref" in schema) {
                return this.resolveRef(schema.$ref);
            }
            else {
                return schema;
            }
        }
    }
}

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

function getClientName(context, type) {
    const viaProjection = getProjectedName(context.program, type, "client");
    const clientName = getClientNameOverride(context.tcgcSdkContext, type);
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
    const { program } = context;
    const explicitOperationId = getOperationId(program, operation);
    if (explicitOperationId) {
        return explicitOperationId;
    }
    const operationName = getClientName(context, operation);
    if (operation.interface) {
        return pascalCaseForOperationId(`${getClientName(context, operation.interface)}_${operationName}`);
    }
    const namespace = operation.namespace;
    if (namespace === undefined ||
        isGlobalNamespace(program, namespace) ||
        isService(program, namespace)) {
        return pascalCase(operationName);
    }
    return pascalCaseForOperationId(`${namespace.name}_${operationName}`);
}
function pascalCaseForOperationId(name) {
    return name
        .split("_")
        .map((s) => pascalCase(s))
        .join("_");
}

/**
 * Represents a node that will hold a JSON reference. The value is computed
 * at the end so that we can defer decisions about the name that is
 * referenced.
 */
class Ref {
    value;
    toJSON() {
        compilerAssert(this.value, "Reference value never set.");
        return this.value;
    }
}
async function getOpenAPIForService(context, options) {
    const { program, service } = context;
    const typeNameOptions = {
        // shorten type names by removing TypeSpec and service namespace
        namespaceFilter(ns) {
            return !isService(program, ns);
        },
    };
    const info = resolveInfo(program, service.type);
    const auth = processAuth(service.type);
    const root = {
        swagger: "2.0",
        info: {
            title: "(title)",
            ...info,
            version: context.version ?? info?.version ?? "0000-00-00",
            "x-typespec-generated": [{ emitter: "@azure-tools/typespec-autorest" }],
        },
        schemes: ["https"],
        ...resolveHost(program, service.type),
        externalDocs: getExternalDocs(program, service.type),
        produces: [], // Pre-initialize produces and consumes so that
        consumes: [], // they show up at the top of the document
        security: auth?.security,
        securityDefinitions: auth?.securitySchemes ?? {},
        tags: [],
        paths: {},
        "x-ms-paths": {},
        definitions: {},
        parameters: {},
    };
    let currentEndpoint;
    let currentConsumes;
    let currentProduces;
    const metadataInfo = createMetadataInfo(program, {
        canonicalVisibility: Visibility.Read,
        canShareProperty: canSharePropertyUsingReadonlyOrXMSMutability,
    });
    // Keep a map of all Types+Visibility combinations that were encountered
    // that need schema definitions.
    const pendingSchemas = new TwoLevelMap();
    // Reuse a single ref object per Type+Visibility combination.
    const refs = new TwoLevelMap();
    // Keep track of inline types still in the process of having their schema computed
    // This is used to detect cycles in inline types, which is an
    const inProgressInlineTypes = new Set();
    // Map model properties that represent shared parameters to their parameter
    // definition that will go in #/parameters. Inlined parameters do not go in
    // this map.
    const params = new Map();
    // Keep track of models that have had properties spread into parameters. We won't
    // consider these unreferenced when emitting unreferenced types.
    const paramModels = new Set();
    // De-dupe the per-endpoint tags that will be added into the #/tags
    const tags = new Set();
    // The set of produces/consumes values found in all operations
    const globalProduces = new Set(["application/json"]);
    const globalConsumes = new Set(["application/json"]);
    const operationIdsWithExample = new Set();
    const [exampleMap, diagnostics] = await loadExamples(program, options, context.version);
    program.reportDiagnostics(diagnostics);
    const httpService = ignoreDiagnostics(getHttpService(program, service.type));
    const routes = httpService.operations;
    reportIfNoRoutes(program, routes);
    routes.forEach(emitOperation);
    emitParameters();
    emitSchemas(service.type);
    emitTags();
    // Finalize global produces/consumes
    if (globalProduces.size > 0) {
        root.produces = [...globalProduces.values()];
    }
    else {
        delete root.produces;
    }
    if (globalConsumes.size > 0) {
        root.consumes = [...globalConsumes.values()];
    }
    else {
        delete root.consumes;
    }
    // Clean up empty entries
    if (root["x-ms-paths"] && Object.keys(root["x-ms-paths"]).length === 0) {
        delete root["x-ms-paths"];
    }
    if (root.security && Object.keys(root.security).length === 0) {
        delete root["security"];
    }
    if (root.securityDefinitions && Object.keys(root.securityDefinitions).length === 0) {
        delete root["securityDefinitions"];
    }
    return {
        document: root,
        operationExamples: [...operationIdsWithExample]
            .map((operationId) => {
            const data = exampleMap.get(operationId);
            if (data) {
                return { operationId, examples: Object.values(data) };
            }
            else {
                return undefined;
            }
        })
            .filter((x) => x),
        outputFile: context.outputFile,
    };
    function resolveHost(program, namespace) {
        const servers = getServers(program, namespace);
        if (servers === undefined) {
            return {};
        }
        // If there is more than one server we then just make a custom host with a parameter asking for the full url.
        if (servers.length > 1) {
            return {
                "x-ms-parameterized-host": {
                    hostTemplate: "{url}",
                    useSchemePrefix: false,
                    parameters: [
                        {
                            name: "url",
                            in: "path",
                            description: "Url",
                            type: "string",
                            format: "uri",
                            "x-ms-skip-url-encoding": true,
                        },
                    ],
                },
            };
        }
        const server = servers[0];
        if (server.parameters.size === 0) {
            const [scheme, host] = server.url.split("://");
            return {
                host,
                schemes: [scheme],
            };
        }
        const parameters = [];
        for (const prop of server.parameters.values()) {
            const param = getOpenAPI2Parameter({
                param: prop,
                type: "path",
                name: prop.name,
                explode: false,
                style: "simple",
                allowReserved: false,
            }, {
                visibility: Visibility.Read,
                ignoreMetadataAnnotations: false,
            });
            if (prop.type.kind === "Scalar" &&
                ignoreDiagnostics(program.checker.isTypeAssignableTo(prop.type.projectionBase ?? prop.type, program.checker.getStdType("url"), prop.type))) {
                param["x-ms-skip-url-encoding"] = true;
            }
            parameters.push(param);
        }
        return {
            "x-ms-parameterized-host": {
                hostTemplate: server.url,
                useSchemePrefix: false,
                parameters,
            },
        };
    }
    function getLastSegment(segments) {
        if (segments) {
            return segments[segments.length - 1];
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
    function resolveXmsPageable(program, operation) {
        if (isList(program, operation.operation)) {
            const pagedInfo = ignoreDiagnostics(getPagingOperation(program, operation.operation));
            return pagedInfo && getXmsPageableForPagingOperation(pagedInfo);
        }
        else {
            return extractAzureCorePagedMetadata(program, operation);
        }
    }
    function getXmsPageableForPagingOperation(paging) {
        if (paging.output.nextLink) {
            const itemsName = paging.output.pageItems.property.name;
            return {
                nextLinkName: paging.output.nextLink.property.name,
                itemName: itemsName === "items" ? undefined : itemsName,
            };
        }
        return undefined;
    }
    function extractAzureCorePagedMetadata(program, operation) {
        for (const response of operation.responses) {
            const paged = extractPagedMetadataNested(program, response.type);
            if (paged) {
                const nextLinkName = getLastSegment(paged.nextLinkSegments);
                const itemName = getLastSegment(paged.itemsSegments);
                if (nextLinkName) {
                    return {
                        nextLinkName,
                        itemName: itemName !== "value" ? itemName : undefined,
                    };
                }
                // Once we find paged metadata, we don't need to processes any further.
                return undefined;
            }
        }
        return undefined;
    }
    function requiresXMsPaths(path, operation) {
        const isShared = isSharedRoute(program, operation) ?? false;
        if (path.includes("?")) {
            return true;
        }
        return isShared;
    }
    function getPathWithoutQuery(path) {
        // strip everything from the key including and after the ?
        return path.replace(/\/?\?.*/, "");
    }
    function getFinalStateVia(metadata) {
        switch (metadata.finalStateVia) {
            case FinalStateValue.azureAsyncOperation:
                return "azure-async-operation";
            case FinalStateValue.location:
                return "location";
            case FinalStateValue.operationLocation:
                return "operation-location";
            case FinalStateValue.originalUri:
                return "original-uri";
            default:
                return undefined;
        }
    }
    function getFinalStateSchema(metadata) {
        if (metadata.finalResult !== undefined &&
            metadata.finalResult !== "void" &&
            metadata.finalResult.name.length > 0) {
            const model = metadata.finalResult;
            const schemaOrRef = resolveExternalRef(metadata.finalResult);
            if (schemaOrRef !== undefined) {
                const ref = new Ref();
                ref.value = schemaOrRef.$ref;
                return { "final-state-schema": ref };
            }
            const pending = pendingSchemas.getOrAdd(metadata.finalResult, Visibility.Read, () => ({
                type: model,
                visibility: Visibility.Read,
                ref: refs.getOrAdd(model, Visibility.Read, () => new Ref()),
            }));
            return { "final-state-schema": pending.ref };
        }
        return undefined;
    }
    function emitOperation(operation) {
        let { path: fullPath, operation: op, verb, parameters } = operation;
        let pathsObject = root.paths;
        const pathWithoutAnyQuery = getPathWithoutQuery(fullPath);
        if (root.paths[pathWithoutAnyQuery]?.[verb] === undefined) {
            fullPath = pathWithoutAnyQuery;
            pathsObject = root.paths;
        }
        else if (requiresXMsPaths(fullPath, op)) {
            // if the key already exists in x-ms-paths, append
            // the operation id.
            if (fullPath.includes("?")) {
                if (root["x-ms-paths"]?.[fullPath] !== undefined) {
                    fullPath += `&_overload=${operation.operation.name}`;
                }
            }
            else {
                fullPath += `?_overload=${operation.operation.name}`;
            }
            pathsObject = root["x-ms-paths"];
        }
        else {
            // This should not happen because http library should have already validated duplicate path or the routes must have been using shared routes and so goes in previous condition.
            compilerAssert(false, `Duplicate route "${fullPath}". This is unexpected.`);
        }
        if (!pathsObject[fullPath]) {
            pathsObject[fullPath] = {};
        }
        const currentPath = pathsObject[fullPath];
        if (!currentPath[verb]) {
            currentPath[verb] = {};
        }
        currentEndpoint = currentPath[verb];
        currentConsumes = new Set();
        currentProduces = new Set();
        const currentTags = getAllTags(program, op);
        if (currentTags) {
            currentEndpoint.tags = currentTags;
            for (const tag of currentTags) {
                // Add to root tags if not already there
                tags.add(tag);
            }
        }
        currentEndpoint.operationId = resolveOperationId(context, op);
        applyExternalDocs(op, currentEndpoint);
        // Set up basic endpoint fields
        currentEndpoint.summary = getSummary(program, op);
        currentEndpoint.description = getDoc(program, op);
        currentEndpoint.parameters = [];
        currentEndpoint.responses = {};
        const lroMetadata = getLroMetadata(program, op);
        // We ignore GET operations because they cannot be LROs per our guidelines and this
        // ensures we don't add the x-ms-long-running-operation extension to the polling operation,
        // which does have LRO metadata.
        if (lroMetadata !== undefined && operation.verb !== "get") {
            currentEndpoint["x-ms-long-running-operation"] = true;
            if (options.emitLroOptions !== "none") {
                const finalState = getFinalStateVia(lroMetadata);
                if (finalState !== undefined) {
                    const finalSchema = getFinalStateSchema(lroMetadata);
                    let lroOptions = {
                        "final-state-via": finalState,
                    };
                    if (finalSchema !== undefined && options.emitLroOptions === "all") {
                        lroOptions = {
                            "final-state-via": finalState,
                            ...finalSchema,
                        };
                    }
                    currentEndpoint["x-ms-long-running-operation-options"] = lroOptions;
                }
            }
        }
        // Extract paged metadata from Azure.Core.Page
        const pageable = resolveXmsPageable(program, operation);
        if (pageable) {
            currentEndpoint["x-ms-pageable"] = pageable;
        }
        const visibility = resolveRequestVisibility(program, operation.operation, verb);
        emitEndpointParameters(parameters, visibility);
        emitResponses(operation.responses);
        applyEndpointConsumes();
        applyEndpointProduces();
        if (isDeprecated(program, op)) {
            currentEndpoint.deprecated = true;
        }
        const examples = getExamples(program, op);
        if (examples) {
            currentEndpoint["x-ms-examples"] = examples.reduce((acc, example) => ({ ...acc, [example.title]: { $ref: example.pathOrUri } }), {});
        }
        const autoExamples = exampleMap.get(currentEndpoint.operationId);
        if (autoExamples && currentEndpoint.operationId) {
            operationIdsWithExample.add(currentEndpoint.operationId);
            currentEndpoint["x-ms-examples"] = currentEndpoint["x-ms-examples"] || {};
            for (const [title, example] of Object.entries(autoExamples)) {
                currentEndpoint["x-ms-examples"][title] = { $ref: `./examples/${example.relativePath}` };
            }
        }
        // Attach additional extensions after main fields
        attachExtensions(op, currentEndpoint);
    }
    function applyEndpointProduces() {
        if (currentProduces.size > 0 && !checkLocalAndGlobalEqual(globalProduces, currentProduces)) {
            currentEndpoint.produces = [...currentProduces];
        }
    }
    function applyEndpointConsumes() {
        if (currentConsumes.size > 0 && !checkLocalAndGlobalEqual(globalConsumes, currentConsumes)) {
            currentEndpoint.consumes = [...currentConsumes];
        }
    }
    function checkLocalAndGlobalEqual(global, local) {
        if (global.size !== local.size) {
            return false;
        }
        for (const entry of local) {
            if (!global.has(entry)) {
                return false;
            }
        }
        return true;
    }
    function isBytes(type) {
        const baseType = type.projectionBase ?? type;
        return ignoreDiagnostics(program.checker.isTypeAssignableTo(baseType, program.checker.getStdType("bytes"), type));
    }
    function isBinaryPayload(body, contentType) {
        const types = new Set(typeof contentType === "string" ? [contentType] : contentType);
        return (body.kind === "Scalar" &&
            body.name === "bytes" &&
            !types.has("application/json") &&
            !types.has("text/plain"));
    }
    function emitResponses(responses) {
        for (const response of responses) {
            for (const statusCode of getOpenAPI2StatusCodes(response.statusCodes, response.type)) {
                emitResponseObject(statusCode, response);
            }
        }
    }
    function getOpenAPI2StatusCodes(statusCodes, diagnosticTarget) {
        if (statusCodes === "*") {
            return ["default"];
        }
        else if (typeof statusCodes === "number") {
            return [String(statusCodes)];
        }
        else {
            return rangeToOpenAPI(statusCodes, diagnosticTarget);
        }
    }
    function rangeToOpenAPI(range, diagnosticTarget) {
        const reportInvalid = () => reportDiagnostic(program, {
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
    function getResponseDescriptionForStatusCode(statusCode) {
        if (statusCode === "default") {
            return "An unexpected error response.";
        }
        return getStatusCodeDescription(statusCode) ?? "unknown";
    }
    function emitResponseObject(statusCode, response) {
        const openapiResponse = currentEndpoint.responses[statusCode] ?? {
            description: response.description ?? getResponseDescriptionForStatusCode(statusCode),
        };
        if (isErrorModel(program, response.type) && statusCode !== "default") {
            openapiResponse["x-ms-error-response"] = true;
        }
        const contentTypes = [];
        let body;
        for (const data of response.responses) {
            if (data.headers && Object.keys(data.headers).length > 0) {
                openapiResponse.headers ??= {};
                for (const [key, value] of Object.entries(data.headers)) {
                    openapiResponse.headers[key] = getResponseHeader(value);
                }
            }
            if (data.body) {
                if (body && body.type !== data.body.type) {
                    reportDiagnostic(program, {
                        code: "duplicate-body-types",
                        target: response.type,
                    });
                }
                body = data.body;
                contentTypes.push(...data.body.contentTypes);
            }
        }
        if (body) {
            openapiResponse.schema = getSchemaForResponseBody(body, contentTypes);
        }
        for (const contentType of contentTypes) {
            currentProduces.add(contentType);
        }
        currentEndpoint.responses[statusCode] = openapiResponse;
    }
    function getSchemaForResponseBody(body, contentTypes) {
        const isBinary = contentTypes.every((t) => isBinaryPayload(body.type, t));
        if (isBinary) {
            return { type: "file" };
        }
        if (body.bodyKind === "multipart") {
            // OpenAPI2 doesn't support multipart responses, so we just return a string schema
            return { type: "string" };
        }
        return getSchemaOrRef(body.type, {
            visibility: Visibility.Read,
            ignoreMetadataAnnotations: body.isExplicit && body.containsMetadataAnnotations,
        });
    }
    function getResponseHeader(prop) {
        const header = getOpenAPI2HeaderParameter(prop, {
            visibility: Visibility.Read,
            ignoreMetadataAnnotations: false,
        });
        Object.assign(header, applyIntrinsicDecorators(prop, {
            type: header.type,
            format: header.format,
        }));
        delete header.in;
        delete header.name;
        delete header["x-ms-client-name"];
        delete header.required;
        return header;
    }
    function expandRef(ref) {
        const absoluteRef = interpolatePath(ref, {
            "arm-types-dir": options.armTypesDir,
        });
        if (getRootLength(absoluteRef) === 0) {
            return absoluteRef; // It is already relative.
        }
        return getRelativePathFromDirectory(getDirectoryPath(context.outputFile), absoluteRef, false);
    }
    function resolveExternalRef(type) {
        const refUrl = getRef(program, type);
        if (refUrl) {
            return {
                $ref: expandRef(refUrl),
            };
        }
        if (isArmCommonType(type) &&
            (type.kind === "Model" ||
                type.kind === "ModelProperty" ||
                type.kind === "Enum" ||
                type.kind === "Union")) {
            const ref = getArmCommonTypeOpenAPIRef(program, type, {
                version: context.version,
                service: context.service,
            });
            if (ref) {
                return {
                    $ref: expandRef(ref),
                };
            }
        }
        return undefined;
    }
    function getSchemaOrRef(type, schemaContext) {
        let schemaNameOverride = undefined;
        const ref = resolveExternalRef(type);
        if (ref) {
            if (options.emitCommonTypesSchema === "never" ||
                !metadataInfo.isTransformed(type, schemaContext.visibility)) {
                return ref;
            }
            // Reference schemas will only be generated when they differ from READ
            schemaNameOverride = (n, v) => `${n}${getVisibilitySuffix(v, Visibility.Read)}`;
        }
        if (type.kind === "Scalar" && program.checker.isStdType(type)) {
            return getSchemaForScalar(type);
        }
        if (type.kind === "String" || type.kind === "Number" || type.kind === "Boolean") {
            // For literal types, we just want to emit them directly as well.
            return getSchemaForLiterals(type);
        }
        if (type.kind === "StringTemplate") {
            return getSchemaForStringTemplate(type);
        }
        if (type.kind === "Intrinsic" && type.name === "unknown") {
            return getSchemaForIntrinsicType(type);
        }
        if (type.kind === "EnumMember") {
            // Enum members are just the OA representation of their values.
            if (typeof type.value === "number") {
                return { type: "number", enum: [type.value] };
            }
            else {
                return { type: "string", enum: [type.value ?? type.name] };
            }
        }
        if (type.kind === "ModelProperty") {
            return resolveProperty(type, schemaContext);
        }
        type = metadataInfo.getEffectivePayloadType(type, schemaContext.visibility);
        const name = getOpenAPITypeName(program, type, typeNameOptions);
        if (shouldInline(program, type)) {
            const schema = getSchemaForInlineType(type, name, schemaContext);
            if (schema === undefined && isErrorType(type)) {
                // Exit early so that syntax errors are exposed.  This error will
                // be caught and handled in emitOpenAPI.
                throw new ErrorTypeFoundError();
            }
            // helps to read output and correlate to TypeSpec
            if (schema && options.includeXTypeSpecName !== "never") {
                schema["x-typespec-name"] = name;
            }
            return schema;
        }
        else {
            // Use shared schema when type is not transformed by visibility from the canonical read visibility.
            if (!metadataInfo.isTransformed(type, schemaContext.visibility)) {
                schemaContext = { ...schemaContext, visibility: Visibility.Read };
            }
            const pending = pendingSchemas.getOrAdd(type, schemaContext.visibility, () => ({
                type,
                visibility: schemaContext.visibility,
                ref: refs.getOrAdd(type, schemaContext.visibility, () => new Ref()),
                getSchemaNameOverride: schemaNameOverride,
            }));
            return { $ref: pending.ref };
        }
    }
    function getSchemaForInlineType(type, name, context) {
        if (inProgressInlineTypes.has(type)) {
            reportDiagnostic(program, {
                code: "inline-cycle",
                format: { type: name },
                target: type,
            });
            return {};
        }
        inProgressInlineTypes.add(type);
        const schema = getSchemaForType(type, context);
        inProgressInlineTypes.delete(type);
        return schema;
    }
    function getParamPlaceholder(property) {
        let spreadParam = false;
        if (property.sourceProperty) {
            // chase our sources all the way back to the first place this property
            // was defined.
            spreadParam = true;
            property = property.sourceProperty;
            while (property.sourceProperty) {
                property = property.sourceProperty;
            }
        }
        const ref = resolveExternalRef(property);
        if (ref) {
            return ref;
        }
        const parameter = params.get(property);
        if (parameter) {
            return parameter;
        }
        const placeholder = {};
        // only parameters inherited by spreading from non-inlined type are shared in #/parameters
        if (spreadParam && property.model && !shouldInline(program, property.model)) {
            params.set(property, placeholder);
            paramModels.add(property.model);
        }
        return placeholder;
    }
    function getJsonName(type) {
        const viaProjection = getProjectedName(program, type, "json");
        const encodedName = resolveEncodedName(program, type, "application/json");
        // Pick the value set via `encodedName` or default back to the legacy projection otherwise.
        // `resolveEncodedName` will return the original name if no @encodedName so we have to do that check
        return encodedName === type.name ? (viaProjection ?? type.name) : encodedName;
    }
    function emitEndpointParameters(methodParams, visibility) {
        const consumes = methodParams.body?.contentTypes ?? [];
        for (const httpOpParam of methodParams.parameters) {
            const shared = params.get(httpOpParam.param);
            if (shared) {
                currentEndpoint.parameters.push(shared);
                continue;
            }
            // eslint-disable-next-line @typescript-eslint/no-deprecated
            if (httpOpParam.type === "header" && isContentTypeHeader(program, httpOpParam.param)) {
                continue;
            }
            if (httpOpParam.type === "cookie") {
                reportDiagnostic(program, { code: "cookies-unsupported", target: httpOpParam.param });
                continue;
            }
            emitParameter(httpOpParam.param, () => getOpenAPI2Parameter(httpOpParam, { visibility, ignoreMetadataAnnotations: false }));
        }
        if (consumes.length === 0 && methodParams.body) {
            // we didn't find an explicit content type anywhere, so infer from body.
            if (getModelOrScalarTypeIfNullable(methodParams.body.type)) {
                consumes.push("application/json");
            }
        }
        for (const consume of consumes) {
            currentConsumes.add(consume);
        }
        if (methodParams.body && !isVoidType(methodParams.body.type)) {
            emitBodyParameters(methodParams.body, visibility);
        }
    }
    function emitBodyParameters(body, visibility) {
        switch (body.bodyKind) {
            case "single":
                emitSingleBodyParameters(body, visibility);
                break;
            case "multipart":
                emitMultipartBodyParameters(body, visibility);
                break;
        }
    }
    function emitSingleBodyParameters(body, visibility) {
        const isBinary = isBinaryPayload(body.type, body.contentTypes);
        const schemaContext = {
            visibility,
            ignoreMetadataAnnotations: body.isExplicit && body.containsMetadataAnnotations,
        };
        const schema = isBinary
            ? { type: "string", format: "binary" }
            : getSchemaOrRef(body.type, schemaContext);
        if (currentConsumes.has("multipart/form-data")) {
            const bodyModelType = body.type;
            // Assert, this should never happen. Rest library guard against that.
            compilerAssert(bodyModelType.kind === "Model", "Body should always be a Model.");
            if (bodyModelType) {
                for (const param of bodyModelType.properties.values()) {
                    emitParameter(param, () => getOpenAPI2FormDataParameter(param, schemaContext, getJsonName(param)));
                }
            }
        }
        else if (body.property) {
            const prop = body.property;
            emitParameter(prop, () => getOpenAPI2BodyParameter(prop, getJsonName(prop), schema));
        }
        else {
            currentEndpoint.parameters.push({
                name: "body",
                in: "body",
                schema,
                required: true,
            });
        }
    }
    function emitMultipartBodyParameters(body, visibility) {
        for (const [index, part] of body.parts.entries()) {
            const partName = part.name ?? `part${index}`;
            let schema = getFormDataSchema(part.body.type, { visibility, ignoreMetadataAnnotations: false }, partName);
            if (schema) {
                if (part.multi) {
                    schema = {
                        type: "array",
                        items: schema.type === "file" ? { type: "string", format: "binary" } : schema,
                    };
                }
                currentEndpoint.parameters.push({
                    name: partName,
                    in: "formData",
                    required: !part.optional,
                    ...schema,
                });
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
    function emitParameter(prop, resolve) {
        if (isNeverType(prop.type)) {
            return;
        }
        const ph = getParamPlaceholder(prop);
        currentEndpoint.parameters.push(ph);
        // If the parameter already has a $ref, don't bother populating it
        if (!("$ref" in ph)) {
            Object.assign(ph, resolve());
        }
    }
    function getSchemaForPrimitiveItems(type, schemaContext, paramName, multipart) {
        const fullSchema = getSchemaForType(type, schemaContext);
        if (fullSchema === undefined) {
            return undefined;
        }
        if (fullSchema.type === "object") {
            reportDiagnostic(program, {
                code: multipart ? "unsupported-multipart-type" : "unsupported-param-type",
                format: { part: paramName },
                target: type,
            });
            return { type: "string" };
        }
        return fullSchema;
    }
    function getFormDataSchema(type, schemaContext, paramName) {
        if (isBytes(type)) {
            return { type: "file" };
        }
        if (type.kind === "Model" && isArrayModelType(program, type)) {
            const elementType = type.indexer.value;
            if (isBytes(elementType)) {
                return { type: "array", items: { type: "string", format: "binary" } };
            }
            const schema = getSchemaForPrimitiveItems(elementType, schemaContext, paramName, true);
            if (schema === undefined) {
                return undefined;
            }
            delete schema.description;
            return {
                type: "array",
                items: schema,
            };
        }
        else {
            const schema = getSchemaForPrimitiveItems(type, schemaContext, paramName, true);
            if (schema === undefined) {
                return undefined;
            }
            return schema;
        }
    }
    function getOpenAPI2ParameterBase(param, name) {
        const base = {
            name: name ?? param.name,
            required: !param.optional,
            description: getDoc(program, param),
        };
        const clientName = getClientName(context, param);
        if (name !== clientName) {
            base["x-ms-client-name"] = clientName;
        }
        attachExtensions(param, base);
        return base;
    }
    function getOpenAPI2BodyParameter(param, name, bodySchema) {
        const result = {
            in: "body",
            ...getOpenAPI2ParameterBase(param, name),
            schema: bodySchema,
        };
        const jsonName = getJsonName(param);
        if (jsonName !== param.name) {
            // Special case to be able to keep pre-existing cases where you have both the body parameter name and x-ms-client-name
            reportDeprecated(program, "Using encodedName for the body property is meaningless. That property is not serialized as Json. If wanting to rename it use @Azure.ClientGenerator.Core.clientName", param.decorators.find((x) => x.definition?.name === "@encodedName")?.node ?? param);
            result.name = jsonName;
            if (!result["x-ms-client-name"]) {
                result["x-ms-client-name"] = param.name;
            }
        }
        else {
            // For body parameter the only value of the name is in the client so no need to keep the original one
            if (result["x-ms-client-name"]) {
                result.name = result["x-ms-client-name"];
                delete result["x-ms-client-name"];
            }
        }
        return result;
    }
    function getOpenAPI2FormDataParameter(param, schemaContext, name) {
        const base = getOpenAPI2ParameterBase(param, name);
        const result = {
            in: "formData",
            ...base,
            ...getFormDataSchema(param.type, schemaContext, base.name),
            default: param.defaultValue && getDefaultValue(param.defaultValue, param),
        };
        Object.assign(result, applyIntrinsicDecorators(param, {
            type: result.type,
            format: result.format,
        }));
        return result;
    }
    function getSimpleParameterSchema(param, schemaContext, name) {
        if (param.type.kind === "Model" && isArrayModelType(program, param.type)) {
            const itemSchema = getSchemaForPrimitiveItems(param.type.indexer.value, schemaContext, name);
            const schema = itemSchema && {
                ...itemSchema,
            };
            delete schema.description;
            return { type: "array", items: schema };
        }
        else {
            return getSchemaForPrimitiveItems(param.type, schemaContext, name);
        }
    }
    function getQueryCollectionFormat(param) {
        if (param.explode) {
            return "multi";
        }
        // eslint-disable-next-line @typescript-eslint/no-deprecated
        let collectionFormat = param.format;
        if (collectionFormat && !["csv", "ssv", "tsv", "pipes", "multi"].includes(collectionFormat)) {
            collectionFormat = undefined;
            reportDiagnostic(program, { code: "invalid-multi-collection-format", target: param.param });
        }
        return collectionFormat;
    }
    function getOpenAPI2QueryParameter(param, schemaContext) {
        const base = getOpenAPI2ParameterBase(param.param, param.name);
        const collectionFormat = getQueryCollectionFormat(param);
        const schema = getSimpleParameterSchema(param.param, schemaContext, base.name);
        return {
            in: "query",
            collectionFormat: collectionFormat === "csv" && schema.items === undefined // If csv
                ? undefined
                : collectionFormat,
            default: param.param.defaultValue && getDefaultValue(param.param.defaultValue, param.param),
            ...base,
            ...schema,
        };
    }
    function getOpenAPI2PathParameter(param, schemaContext) {
        const base = getOpenAPI2ParameterBase(param.param, param.name);
        const result = {
            in: "path",
            default: param.param.defaultValue && getDefaultValue(param.param.defaultValue, param.param),
            ...base,
            ...getSimpleParameterSchema(param.param, schemaContext, base.name),
        };
        if (param.allowReserved) {
            result["x-ms-skip-url-encoding"] = true;
        }
        return result;
    }
    function getOpenAPI2HeaderParameter(param, schemaContext, name) {
        const base = getOpenAPI2ParameterBase(param, name);
        let collectionFormat = getHeaderFieldOptions(program, param).format;
        if (collectionFormat && !["csv", "ssv", "tsv", "pipes"].includes(collectionFormat)) {
            collectionFormat = undefined;
            reportDiagnostic(program, { code: "invalid-multi-collection-format", target: param });
        }
        return {
            in: "header",
            default: param.defaultValue && getDefaultValue(param.defaultValue, param),
            ...base,
            collectionFormat: collectionFormat,
            ...getSimpleParameterSchema(param, schemaContext, base.name),
        };
    }
    function getOpenAPI2ParameterInternal(param, schemaContext) {
        switch (param.type) {
            case "query":
                return getOpenAPI2QueryParameter(param, schemaContext);
            case "path":
                return getOpenAPI2PathParameter(param, schemaContext);
            case "header":
                return getOpenAPI2HeaderParameter(param.param, schemaContext, param.name);
            case "cookie":
                compilerAssert(false, "Should verify cookies before");
                break;
            default:
                compilerAssert(false, "Unreachable");
        }
    }
    function getOpenAPI2Parameter(param, schemaContext) {
        const value = getOpenAPI2ParameterInternal(param, schemaContext);
        // Apply decorators to a copy of the parameter definition.  We use
        // Object.assign here because applyIntrinsicDecorators returns a new object
        // based on the target object and we need to apply its changes back to the
        // original parameter.
        Object.assign(value, applyIntrinsicDecorators(param.param, {
            type: value.type,
            format: value.format,
        }));
        return value;
    }
    function emitParameters() {
        for (const [property, param] of params) {
            // Add an extension which tells AutoRest that this is a shared operation
            // parameter definition
            if (param["x-ms-parameter-location"] === undefined) {
                param["x-ms-parameter-location"] = "method";
            }
            const key = getParameterKey(program, property, param, root.parameters, typeNameOptions);
            root.parameters[key] = { ...param };
            const refedParam = param;
            for (const key of Object.keys(param)) {
                delete refedParam[key];
            }
            refedParam["$ref"] = "#/parameters/" + encodeURIComponent(key);
        }
    }
    function emitSchemas(serviceNamespace) {
        const processedSchemas = new TwoLevelMap();
        processSchemas();
        if (!options.omitUnreachableTypes) {
            processUnreferencedSchemas();
        }
        // Emit the processed schemas. Only now can we compute the names as it
        // depends on whether we have produced multiple schemas for a single
        // TYPESPEC type.
        for (const group of processedSchemas.values()) {
            for (const [visibility, processed] of group) {
                let name = getClientNameOverride(context.tcgcSdkContext, processed.type);
                if (name === undefined) {
                    name = getOpenAPITypeName(program, processed.type, typeNameOptions);
                }
                if (processed.getSchemaNameOverride !== undefined) {
                    name = processed.getSchemaNameOverride(name, visibility);
                }
                else if (group.size > 1) {
                    name += getVisibilitySuffix(visibility, Visibility.Read);
                }
                checkDuplicateTypeName(program, processed.type, name, root.definitions);
                processed.ref.value = "#/definitions/" + encodeURIComponent(name);
                if (processed.schema) {
                    root.definitions[name] = processed.schema;
                }
            }
        }
        function processSchemas() {
            // Process pending schemas. Note that getSchemaForType may pull in new
            // pending schemas so we iterate until there are no pending schemas
            // remaining.
            while (pendingSchemas.size > 0) {
                for (const [type, group] of pendingSchemas) {
                    for (const [visibility, pending] of group) {
                        processedSchemas.getOrAdd(type, visibility, () => ({
                            ...pending,
                            schema: getSchemaForType(type, {
                                visibility: visibility,
                                ignoreMetadataAnnotations: false,
                            }),
                        }));
                    }
                    pendingSchemas.delete(type);
                }
            }
        }
        function processUnreferencedSchemas() {
            const addSchema = (type) => {
                if (!processedSchemas.has(type) &&
                    !paramModels.has(type) &&
                    !shouldInline(program, type) &&
                    !shouldOmitThisUnreachableType(type)) {
                    getSchemaOrRef(type, { visibility: Visibility.Read, ignoreMetadataAnnotations: false });
                }
            };
            const skipSubNamespaces = isGlobalNamespace(program, serviceNamespace);
            navigateTypesInNamespace(serviceNamespace, {
                model: addSchema,
                scalar: addSchema,
                enum: addSchema,
                union: addSchema,
            }, { skipSubNamespaces });
            processSchemas();
        }
        function shouldOmitThisUnreachableType(type) {
            if (options.versionEnumStrategy !== "include" &&
                type.kind === "Enum" &&
                isVersionEnum(program, type)) {
                return true;
            }
            return false;
        }
    }
    function isVersionEnum(program, enumObj) {
        const [_, map] = getVersionsForEnum(program, enumObj);
        if (map !== undefined && map.getVersions()[0].enumMember.enum === enumObj) {
            return true;
        }
        return false;
    }
    function emitTags() {
        for (const tag of tags) {
            root.tags.push({ name: tag });
        }
    }
    function getSchemaForType(type, schemaContext) {
        const builtinType = getSchemaForLiterals(type);
        if (builtinType !== undefined) {
            return builtinType;
        }
        switch (type.kind) {
            case "Intrinsic":
                return getSchemaForIntrinsicType(type);
            case "Model":
                return getSchemaForModel(type, schemaContext);
            case "ModelProperty":
                return getSchemaForType(type.type, schemaContext);
            case "Scalar":
                return getSchemaForScalar(type);
            case "Union":
                return getSchemaForUnion(type, schemaContext);
            case "UnionVariant":
                return getSchemaForUnionVariant(type, schemaContext);
            case "Enum":
                return getSchemaForEnum(type);
            case "Tuple":
                return { type: "array", items: {} };
        }
        reportDiagnostic(program, {
            code: "invalid-schema",
            format: { type: type.kind },
            target: type,
        });
        return undefined;
    }
    function getSchemaForIntrinsicType(type) {
        switch (type.name) {
            case "unknown":
                return {};
        }
        reportDiagnostic(program, {
            code: "invalid-schema",
            format: { type: type.name },
            target: type,
        });
        return {};
    }
    /**
     * Version enum is special so we we just render the current version with modelAsString: true
     */
    function getSchemaForVersionEnum(e, currentVersion) {
        const member = [...e.members.values()].find((x) => (x.value ?? x.name) === currentVersion);
        compilerAssert(member, `Version enum ${e.name} does not have a member for ${currentVersion}.`, e);
        return {
            type: "string",
            description: getDoc(program, e),
            enum: [member.value ?? member.name],
            "x-ms-enum": {
                name: e.name,
                modelAsString: true,
                values: [
                    {
                        name: member.name,
                        value: member.value ?? member.name,
                        description: getDoc(program, member),
                    },
                ],
            },
        };
    }
    function getSchemaForEnum(e) {
        const values = [];
        if (e.members.size === 0) {
            reportUnsupportedUnion("empty");
            return {};
        }
        const type = getEnumMemberType(e.members.values().next().value);
        for (const option of e.members.values()) {
            if (type !== getEnumMemberType(option)) {
                reportUnsupportedUnion();
                continue;
            }
            else {
                values.push(option.value ?? option.name);
            }
        }
        // If we are rendering a specific version and trying to render the version enum we should treat it specially to only include the current version.
        if (isVersionEnum(program, e) && context.version) {
            return getSchemaForVersionEnum(e, context.version);
        }
        const schema = { type, description: getDoc(program, e) };
        if (values.length > 0) {
            schema.enum = values;
            addXMSEnum(e, schema);
        }
        if (options.useReadOnlyStatusSchema) {
            const [values, _] = extractLroStates(program, e);
            if (values !== undefined) {
                schema.readOnly = true;
            }
        }
        return schema;
        function getEnumMemberType(member) {
            if (typeof member.value === "number") {
                return "number";
            }
            return "string";
        }
        function reportUnsupportedUnion(messageId = "default") {
            reportDiagnostic(program, { code: "union-unsupported", messageId, target: e });
        }
    }
    function getSchemaForUnionEnum(union, e) {
        const values = [];
        let foundCustom = false;
        for (const [name, member] of e.flattenedMembers.entries()) {
            const description = getDoc(program, member.type);
            const memberClientName = getClientNameOverride(context.tcgcSdkContext, member.type);
            values.push({
                name: memberClientName ?? (typeof name === "string" ? name : `${member.value}`),
                value: member.value,
                description,
            });
            if (description || typeof name === "string") {
                foundCustom = true;
            }
        }
        const schema = {
            type: e.kind,
            enum: [...e.flattenedMembers.values()].map((x) => x.value),
            "x-ms-enum": {
                name: union.name,
                modelAsString: e.open,
            },
        };
        if (foundCustom) {
            schema["x-ms-enum"].values = values;
        }
        if (e.nullable) {
            schema["x-nullable"] = true;
        }
        if (options.useReadOnlyStatusSchema) {
            const [values, _] = extractLroStates(program, union);
            if (values !== undefined) {
                schema.readOnly = true;
            }
        }
        return applyIntrinsicDecorators(union, schema);
    }
    function getSchemaForUnion(union, schemaContext) {
        const nonNullOptions = [...union.variants.values()]
            .map((x) => x.type)
            .filter((t) => !isNullType(t));
        const nullable = union.variants.size !== nonNullOptions.length;
        if (nonNullOptions.length === 0) {
            reportDiagnostic(program, { code: "union-null", target: union });
            return {};
        }
        if (nonNullOptions.length === 1) {
            const type = nonNullOptions[0];
            // Get the schema for the model type
            const schema = getSchemaOrRef(type, schemaContext);
            if (schema.$ref) {
                if (type.kind === "Model") {
                    return { type: "object", allOf: [schema], "x-nullable": nullable };
                }
                else {
                    return { ...schema, "x-nullable": nullable };
                }
            }
            else {
                schema["x-nullable"] = nullable;
                return schema;
            }
        }
        else {
            const [asEnum, _] = getUnionAsEnum(union);
            if (asEnum) {
                return getSchemaForUnionEnum(union, asEnum);
            }
            reportDiagnostic(program, {
                code: "union-unsupported",
                target: union,
            });
            return {};
        }
    }
    function ifArrayItemContainsIdentifier(program, array) {
        if (array.indexer.value?.kind !== "Model") {
            return true;
        }
        return (getExtensions(program, array).has("x-ms-identifiers") ||
            getProperty(array.indexer.value, "id"));
    }
    function getSchemaForUnionVariant(variant, schemaContext) {
        return getSchemaForType(variant.type, schemaContext);
    }
    function getDefaultValue(defaultType, modelProperty) {
        return serializeValueAsJson(program, defaultType, modelProperty);
    }
    function includeDerivedModel(model) {
        return (!resolveExternalRef(model) &&
            !isTemplateDeclaration(model) &&
            (model.templateMapper?.args === undefined ||
                model.templateMapper?.args.length === 0 ||
                model.derivedModels.length > 0));
    }
    function getDiscriminatorValue(model) {
        let discriminator;
        let current = model;
        while (current.baseModel) {
            discriminator = getDiscriminator(program, current.baseModel);
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
                return values[0];
            }
        }
        return undefined;
    }
    function getSchemaForModel(model, schemaContext) {
        const array = getArrayType(model, schemaContext);
        if (array) {
            return array;
        }
        const modelSchema = {
            type: "object",
            description: getDoc(program, model),
        };
        if (model.baseModel) {
            const discriminatorValue = getDiscriminatorValue(model);
            if (discriminatorValue) {
                const extensions = getExtensions(program, model);
                if (!extensions.has("x-ms-discriminator-value")) {
                    modelSchema["x-ms-discriminator-value"] = discriminatorValue;
                }
            }
        }
        const properties = {};
        if (isRecordModelType(program, model)) {
            modelSchema.additionalProperties = getSchemaOrRef(model.indexer.value, schemaContext);
        }
        const derivedModels = resolveExternalRef(model)
            ? []
            : model.derivedModels.filter(includeDerivedModel);
        // getSchemaOrRef on all children to push them into components.schemas
        for (const child of derivedModels) {
            getSchemaOrRef(child, schemaContext);
        }
        const discriminator = getDiscriminator(program, model);
        if (discriminator) {
            const { propertyName } = discriminator;
            modelSchema.discriminator = propertyName;
            // Push discriminator into base type, but only if it is not already there
            if (!model.properties.get(propertyName)) {
                properties[propertyName] = {
                    type: "string",
                    description: `Discriminator property for ${model.name}.`,
                };
                modelSchema.required = [propertyName];
            }
        }
        applySummary(model, modelSchema);
        applyExternalDocs(model, modelSchema);
        for (const prop of model.properties.values()) {
            if (!metadataInfo.isPayloadProperty(prop, schemaContext.visibility, schemaContext.ignoreMetadataAnnotations)) {
                continue;
            }
            if (isNeverType(prop.type)) {
                // If the property has a type of 'never', don't include it in the schema
                continue;
            }
            const jsonName = getJsonName(prop);
            const clientName = getClientName(context, prop);
            const description = getDoc(program, prop);
            // if this property is a discriminator property, remove it to keep autorest validation happy
            if (model.baseModel) {
                const { propertyName } = getDiscriminator(program, model.baseModel) || {};
                if (jsonName === propertyName) {
                    continue;
                }
            }
            if (!metadataInfo.isOptional(prop, schemaContext.visibility) ||
                prop.name === discriminator?.propertyName) {
                if (!modelSchema.required) {
                    modelSchema.required = [];
                }
                modelSchema.required.push(jsonName);
            }
            // Apply decorators on the property to the type's schema
            properties[jsonName] = resolveProperty(prop, schemaContext);
            const property = properties[jsonName];
            if (jsonName !== clientName) {
                property["x-ms-client-name"] = clientName;
            }
            if (description) {
                property.description = description;
            }
            applySummary(prop, property);
            if (prop.defaultValue && !("$ref" in property)) {
                property.default = getDefaultValue(prop.defaultValue, prop);
            }
            if (isReadonlyProperty(program, prop)) {
                property.readOnly = true;
            }
            else {
                // eslint-disable-next-line @typescript-eslint/no-deprecated
                const vis = getVisibility(program, prop);
                if (vis) {
                    const mutability = [];
                    if (vis.includes("read")) {
                        mutability.push("read");
                    }
                    if (vis.includes("update")) {
                        mutability.push("update");
                    }
                    if (vis.includes("create")) {
                        mutability.push("create");
                    }
                    if (mutability.length > 0) {
                        property["x-ms-mutability"] = mutability;
                    }
                }
            }
            // Attach any additional OpenAPI extensions
            attachExtensions(prop, property);
        }
        // Special case: if a model type extends a single *templated* base type and
        // has no properties of its own, absorb the definition of the base model
        // into this schema definition.  The assumption here is that any model type
        // defined like this is just meant to rename the underlying instance of a
        // templated type.
        if (model.baseModel &&
            isTemplateDeclarationOrInstance(model.baseModel) &&
            Object.keys(properties).length === 0) {
            // Take the base model schema but carry across the documentation property
            // that we set before
            const baseSchema = getSchemaForType(model.baseModel, schemaContext);
            Object.assign(modelSchema, baseSchema, { description: modelSchema.description });
        }
        else if (model.baseModel) {
            const baseSchema = getSchemaOrRef(model.baseModel, schemaContext);
            modelSchema.allOf = [baseSchema];
        }
        if (Object.keys(properties).length > 0) {
            modelSchema.properties = properties;
        }
        // Attach any OpenAPI extensions
        attachExtensions(model, modelSchema);
        return modelSchema;
    }
    function canSharePropertyUsingReadonlyOrXMSMutability(prop) {
        const sharedVisibilities = ["read", "create", "update", "write"];
        // eslint-disable-next-line @typescript-eslint/no-deprecated
        const visibilities = getVisibility(program, prop);
        if (visibilities) {
            for (const visibility of visibilities) {
                if (!sharedVisibilities.includes(visibility)) {
                    return false;
                }
            }
        }
        return true;
    }
    function resolveProperty(prop, context) {
        let propSchema;
        if (prop.type.kind === "Enum" && prop.defaultValue) {
            propSchema = getSchemaForEnum(prop.type);
        }
        else if (prop.type.kind === "Union" && prop.defaultValue) {
            const [asEnum, _] = getUnionAsEnum(prop.type);
            if (asEnum) {
                propSchema = getSchemaForUnionEnum(prop.type, asEnum);
            }
            else {
                propSchema = getSchemaOrRef(prop.type, context);
            }
        }
        else {
            propSchema = getSchemaOrRef(prop.type, context);
        }
        if (options.armResourceFlattening && isConditionallyFlattened(program, prop)) {
            return { ...applyIntrinsicDecorators(prop, propSchema), "x-ms-client-flatten": true };
        }
        else {
            return applyIntrinsicDecorators(prop, propSchema);
        }
    }
    function attachExtensions(type, emitObject) {
        // Attach any OpenAPI extensions
        const extensions = getExtensions(program, type);
        if (isAzureResource(program, type)) {
            emitObject["x-ms-azure-resource"] = true;
        }
        if (getAsEmbeddingVector(program, type) !== undefined) {
            emitObject["x-ms-embedding-vector"] = true;
        }
        if (type.kind === "Scalar") {
            const ext = getArmResourceIdentifierConfig(program, type);
            if (ext) {
                emitObject["x-ms-arm-id-details"] = ext;
            }
        }
        if (extensions) {
            for (const key of extensions.keys()) {
                emitObject[key] = extensions.get(key);
            }
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
    function applyIntrinsicDecorators(typespecType, target) {
        const newTarget = { ...target };
        const docStr = getDoc(program, typespecType);
        const isString = (typespecType.kind === "Scalar" || typespecType.kind === "ModelProperty") &&
            isStringType(program, getPropertyType(typespecType));
        const isNumeric = (typespecType.kind === "Scalar" || typespecType.kind === "ModelProperty") &&
            isNumericType(program, getPropertyType(typespecType));
        if (docStr) {
            newTarget.description = docStr;
        }
        const title = getSummary(program, typespecType);
        if (title) {
            target.title = title;
        }
        const formatStr = getFormat(program, typespecType);
        if (isString && formatStr) {
            const allowedStringFormats = [
                "char",
                "binary",
                "byte",
                "certificate",
                "date",
                "time",
                "date-time",
                "date-time-rfc1123",
                "date-time-rfc7231",
                "duration",
                "password",
                "uuid",
                "base64url",
                "uri",
                "url",
                "arm-id",
            ];
            if (!allowedStringFormats.includes(formatStr.toLowerCase())) {
                reportDiagnostic(program, {
                    code: "invalid-format",
                    format: { schema: "string", format: formatStr },
                    target: typespecType,
                });
            }
            else {
                newTarget.format = formatStr;
            }
        }
        const pattern = getPattern(program, typespecType);
        if (isString && pattern) {
            newTarget.pattern = pattern;
        }
        const minLength = getMinLength(program, typespecType);
        if (isString && minLength !== undefined) {
            newTarget.minLength = minLength;
        }
        const maxLength = getMaxLength(program, typespecType);
        if (isString && maxLength !== undefined) {
            newTarget.maxLength = maxLength;
        }
        const minValue = getMinValue(program, typespecType);
        if (isNumeric && minValue !== undefined) {
            newTarget.minimum = minValue;
        }
        const maxValue = getMaxValue(program, typespecType);
        if (isNumeric && maxValue !== undefined) {
            newTarget.maximum = maxValue;
        }
        const minItems = getMinItems(program, typespecType);
        if (!target.minItems && minItems !== undefined) {
            newTarget.minItems = minItems;
        }
        const maxItems = getMaxItems(program, typespecType);
        if (!target.maxItems && maxItems !== undefined) {
            newTarget.maxItems = maxItems;
        }
        if (isSecret(program, typespecType)) {
            newTarget.format = "password";
            newTarget["x-ms-secret"] = true;
        }
        if (isString) {
            const values = getKnownValues(program, typespecType);
            if (values) {
                const enumSchema = { ...newTarget, ...getSchemaForEnum(values) };
                enumSchema["x-ms-enum"].modelAsString = true;
                enumSchema["x-ms-enum"].name = getPropertyType(typespecType).name;
                return enumSchema;
            }
        }
        if (typespecType.kind === "ModelProperty" &&
            shouldFlattenProperty(context.tcgcSdkContext, typespecType)) {
            newTarget["x-ms-client-flatten"] = true;
        }
        attachExtensions(typespecType, newTarget);
        return typespecType.kind === "Scalar" || typespecType.kind === "ModelProperty"
            ? applyEncoding(typespecType, newTarget)
            : newTarget;
    }
    function applyEncoding(typespecType, target) {
        const encodeData = getEncode(program, typespecType);
        if (encodeData) {
            const newTarget = { ...target };
            const newType = getSchemaForScalar(encodeData.type);
            newTarget.type = newType.type;
            // If the target already has a format it takes priority. (e.g. int32)
            newTarget.format = mergeFormatAndEncoding(newTarget.format, encodeData.encoding, newType.format);
            return newTarget;
        }
        return target;
    }
    function mergeFormatAndEncoding(format, encoding, encodeAsFormat) {
        switch (format) {
            case undefined:
                return encodeAsFormat ?? encoding ?? format;
            case "date-time":
                switch (encoding) {
                    case "rfc3339":
                        return "date-time";
                    case "unixTimestamp":
                        return "unixtime";
                    case "rfc7231":
                        return "date-time-rfc7231";
                    default:
                        return encoding;
                }
            case "duration":
                switch (encoding) {
                    case "ISO8601":
                        return "duration";
                    default:
                        return encodeAsFormat ?? encoding;
                }
            default:
                return encodeAsFormat ?? encoding ?? format;
        }
    }
    function applySummary(typespecType, target) {
        const summary = getSummary(program, typespecType);
        if (summary) {
            target.title = summary;
        }
    }
    function applyExternalDocs(typespecType, target) {
        const externalDocs = getExternalDocs(program, typespecType);
        if (externalDocs) {
            target.externalDocs = externalDocs;
        }
    }
    function addXMSEnum(type, schema) {
        if (type.node && type.node.parent && type.node.parent.kind === SyntaxKind.ModelStatement) {
            schema["x-ms-enum"] = {
                name: type.node.parent.id.sv,
                modelAsString: false,
            };
        }
        else if (type.kind === "String") {
            schema["x-ms-enum"] = {
                modelAsString: false,
            };
        }
        else if (type.kind === "Enum") {
            schema["x-ms-enum"] = {
                name: type.name,
                modelAsString: false,
            };
            const values = [];
            let foundCustom = false;
            for (const member of type.members.values()) {
                const description = getDoc(program, member);
                const memberClientName = getClientName(context, member);
                values.push({
                    name: member.name,
                    value: member.value ?? memberClientName,
                    description,
                });
                if (description || member.value !== undefined) {
                    foundCustom = true;
                }
            }
            if (foundCustom) {
                schema["x-ms-enum"].values = values;
            }
        }
        return schema;
    }
    function getSchemaForStringTemplate(stringTemplate) {
        if (stringTemplate.stringValue === undefined) {
            program.reportDiagnostics(explainStringTemplateNotSerializable(stringTemplate).map((x) => ({
                ...x,
                severity: "warning",
            })));
            return { type: "string" };
        }
        return { type: "string", enum: [stringTemplate.stringValue] };
    }
    function getSchemaForLiterals(typespecType) {
        switch (typespecType.kind) {
            case "Number":
                return { type: "number", enum: [typespecType.value] };
            case "String":
                return addXMSEnum(typespecType, { type: "string", enum: [typespecType.value] });
            case "Boolean":
                return { type: "boolean", enum: [typespecType.value] };
            default:
                return undefined;
        }
    }
    /**
     * If the model is an array model return the OpenAPI2Schema for the array type.
     */
    function getArrayType(typespecType, context) {
        if (isArrayModelType(program, typespecType)) {
            const array = {
                type: "array",
                items: getSchemaOrRef(typespecType.indexer.value, {
                    ...context,
                    visibility: context.visibility | Visibility.Item,
                }),
            };
            if (!ifArrayItemContainsIdentifier(program, typespecType)) {
                array["x-ms-identifiers"] = [];
            }
            return applyIntrinsicDecorators(typespecType, array);
        }
        return undefined;
    }
    function getSchemaForScalar(scalar) {
        let result = {};
        const isStd = program.checker.isStdType(scalar);
        if (isStd) {
            result = getSchemaForStdScalars(scalar);
        }
        else if (scalar.baseScalar) {
            result = getSchemaForScalar(scalar.baseScalar);
        }
        const withDecorators = applyIntrinsicDecorators(scalar, result);
        if (isStd) {
            // Standard types are going to be inlined in the spec and we don't want the description of the scalar to show up
            delete withDecorators.description;
        }
        return withDecorators;
    }
    function getSchemaForStdScalars(scalar) {
        function reportNonspecificScalar(scalarName, chosenScalarName) {
            reportDiagnostic(program, {
                code: "nonspecific-scalar",
                format: { type: scalarName, chosenType: chosenScalarName },
                target: scalar,
            });
        }
        switch (scalar.name) {
            case "bytes":
                return { type: "string", format: "byte" };
            case "numeric":
                reportNonspecificScalar("numeric", "int64");
                return { type: "integer", format: "int64" };
            case "integer":
                reportNonspecificScalar("integer", "int64");
                return { type: "integer", format: "int64" };
            case "int8":
                return { type: "integer", format: "int8" };
            case "int16":
                return { type: "integer", format: "int16" };
            case "int32":
                return { type: "integer", format: "int32" };
            case "int64":
                return { type: "integer", format: "int64" };
            case "safeint":
                return { type: "integer", format: "int64" };
            case "uint8":
                return { type: "integer", format: "uint8" };
            case "uint16":
                return { type: "integer", format: "uint16" };
            case "uint32":
                return { type: "integer", format: "uint32" };
            case "uint64":
                return { type: "integer", format: "uint64" };
            case "float":
                reportNonspecificScalar("float", "float64");
                return { type: "number" };
            case "float64":
                return { type: "number", format: "double" };
            case "float32":
                return { type: "number", format: "float" };
            case "decimal":
                return { type: "number", format: "decimal" };
            case "decimal128":
                return { type: "number", format: "decimal" };
            case "string":
                return { type: "string" };
            case "boolean":
                return { type: "boolean" };
            case "plainDate":
                return { type: "string", format: "date" };
            case "utcDateTime":
            case "offsetDateTime":
                return { type: "string", format: "date-time" };
            case "plainTime":
                return { type: "string", format: "time" };
            case "duration":
                return { type: "string", format: "duration" };
            case "url":
                return { type: "string", format: "uri" };
            default:
                scalar.name;
                return {};
        }
    }
    function processAuth(serviceNamespace) {
        const authentication = getAuthentication(program, serviceNamespace);
        if (authentication) {
            return processServiceAuthentication(authentication, serviceNamespace);
        }
        return undefined;
    }
    function processServiceAuthentication(authentication, serviceNamespace) {
        const oaiSchemes = {};
        const security = [];
        for (const option of authentication.options) {
            const oai3SecurityOption = {};
            for (const scheme of option.schemes) {
                const result = getOpenAPI2Scheme(scheme, serviceNamespace);
                if (result !== undefined) {
                    const [oaiScheme, scopes] = result;
                    oaiSchemes[scheme.id] = oaiScheme;
                    oai3SecurityOption[scheme.id] = scopes;
                }
            }
            if (Object.keys(oai3SecurityOption).length > 0) {
                security.push(oai3SecurityOption);
            }
        }
        return { securitySchemes: oaiSchemes, security };
    }
    function getOpenAPI2Scheme(auth, serviceNamespace) {
        switch (auth.type) {
            case "http":
                if (auth.scheme !== "basic") {
                    reportDiagnostic(program, {
                        code: "unsupported-http-auth-scheme",
                        target: serviceNamespace,
                        format: { scheme: auth.scheme },
                    });
                    return undefined;
                }
                return [{ type: "basic", description: auth.description }, []];
            case "apiKey":
                if (auth.in === "cookie") {
                    return undefined;
                }
                return [
                    { type: "apiKey", description: auth.description, in: auth.in, name: auth.name },
                    [],
                ];
            case "oauth2":
                const flow = auth.flows[0];
                if (flow === undefined) {
                    return undefined;
                }
                const oaiFlowName = getOpenAPI2Flow(flow.type);
                return [
                    {
                        type: "oauth2",
                        description: auth.description,
                        flow: oaiFlowName,
                        authorizationUrl: flow.authorizationUrl,
                        tokenUrl: flow.tokenUrl,
                        scopes: Object.fromEntries(flow.scopes.map((x) => [x.value, x.description ?? ""])),
                    },
                    flow.scopes.map((x) => x.value),
                ];
            case "openIdConnect":
            default:
                reportDiagnostic(program, {
                    code: "unsupported-auth",
                    format: { authType: auth.type },
                    target: service.type,
                });
                return undefined;
        }
    }
    function getOpenAPI2Flow(flow) {
        switch (flow) {
            case "authorizationCode":
                return "accessCode";
            case "clientCredentials":
                return "application";
            case "implicit":
                return "implicit";
            case "password":
                return "password";
            default:
                compilerAssert(false, "Unreachable");
        }
    }
}
class ErrorTypeFoundError extends Error {
    constructor() {
        super("Error type found in evaluated TypeSpec output");
    }
}
function sortOpenAPIDocument(doc) {
    // Doing this to make sure the classes with toJSON are resolved.
    const unsorted = JSON.parse(JSON.stringify(doc));
    const sorted = sortWithJsonSchema(unsorted, AutorestOpenAPISchema);
    return sorted;
}
async function checkExamplesDirExists(host, dir) {
    try {
        return (await host.stat(dir)).isDirectory();
    }
    catch (err) {
        return false;
    }
}
async function searchExampleJsonFiles(program, exampleDir) {
    const host = program.host;
    const exampleFiles = [];
    // Recursive file search
    async function recursiveSearch(dir) {
        const fileItems = await host.readDir(dir);
        for (const item of fileItems) {
            const fullPath = joinPaths(dir, item);
            const relativePath = getRelativePathFromDirectory(exampleDir, fullPath, false);
            if ((await host.stat(fullPath)).isDirectory()) {
                await recursiveSearch(fullPath);
            }
            else if ((await host.stat(fullPath)).isFile() &&
                getAnyExtensionFromPath(item) === ".json") {
                exampleFiles.push(normalizePath(relativePath));
            }
        }
    }
    await recursiveSearch(exampleDir);
    return exampleFiles;
}
async function loadExamples(program, options, version) {
    const host = program.host;
    const diagnostics = createDiagnosticCollector();
    const examplesBaseDir = options.examplesDirectory ?? resolvePath(program.projectRoot, "examples");
    const exampleDir = version ? resolvePath(examplesBaseDir, version) : resolvePath(examplesBaseDir);
    if (!(await checkExamplesDirExists(host, exampleDir))) {
        if (options.examplesDirectory) {
            diagnostics.add(createDiagnostic({
                code: "example-loading",
                messageId: "noDirectory",
                format: { directory: exampleDir },
                target: NoTarget,
            }));
        }
        return diagnostics.wrap(new Map());
    }
    const map = new Map();
    const exampleFiles = await searchExampleJsonFiles(program, exampleDir);
    for (const fileName of exampleFiles) {
        try {
            const exampleFile = await host.readFile(resolvePath(exampleDir, fileName));
            const example = JSON.parse(exampleFile.text);
            if (!example.operationId || !example.title) {
                diagnostics.add(createDiagnostic({
                    code: "example-loading",
                    messageId: "noOperationId",
                    format: { filename: fileName },
                    target: { file: exampleFile, pos: 0, end: 0 },
                }));
                continue;
            }
            if (!map.has(example.operationId)) {
                map.set(example.operationId, {});
            }
            const examples = map.get(example.operationId);
            if (example.title in examples) {
                diagnostics.add(createDiagnostic({
                    code: "duplicate-example-file",
                    target: { file: exampleFile, pos: 0, end: 0 },
                    format: {
                        filename: fileName,
                        operationId: example.operationId,
                        title: example.title,
                    },
                }));
            }
            examples[example.title] = {
                relativePath: fileName,
                file: exampleFile,
                data: example,
            };
        }
        catch (err) {
            diagnostics.add(createDiagnostic({
                code: "example-loading",
                messageId: "default",
                format: { filename: fileName, error: err?.toString() ?? "" },
                target: NoTarget,
            }));
        }
    }
    return diagnostics.wrap(map);
}

const defaultOptions = {
    "output-file": "{azure-resource-provider-folder}/{service-name}/{version-status}/{version}/openapi.json",
    "new-line": "lf",
    "include-x-typespec-name": "never",
};
async function $onEmit(context) {
    const tracer = getTracer(context.program);
    const options = resolveAutorestOptions(context.program, context.emitterOutputDir, context.options);
    tracer.trace("options", JSON.stringify(options, null, 2));
    await emitAllServiceAtAllVersions(context.program, options);
}
function resolveAutorestOptions(program, emitterOutputDir, options) {
    const resolvedOptions = {
        ...defaultOptions,
        ...options,
    };
    const armTypesDir = interpolatePath(resolvedOptions["arm-types-dir"] ?? "{project-root}/../../common-types/resource-management", {
        "project-root": program.projectRoot,
        "emitter-output-dir": emitterOutputDir,
    });
    if (resolvedOptions["examples-directory"]) {
        reportDeprecated(program, `examples-directory option is deprecated use examples-dir instead or remove it if examples are located in {project-root}/examples`, NoTarget);
    }
    return {
        outputFile: resolvedOptions["output-file"],
        outputDir: emitterOutputDir,
        azureResourceProviderFolder: resolvedOptions["azure-resource-provider-folder"],
        examplesDirectory: resolvedOptions["examples-dir"] ?? resolvedOptions["examples-directory"],
        version: resolvedOptions["version"],
        newLine: resolvedOptions["new-line"],
        omitUnreachableTypes: resolvedOptions["omit-unreachable-types"],
        versionEnumStrategy: resolvedOptions["version-enum-strategy"],
        includeXTypeSpecName: resolvedOptions["include-x-typespec-name"],
        armTypesDir,
        useReadOnlyStatusSchema: resolvedOptions["use-read-only-status-schema"],
        emitLroOptions: resolvedOptions["emit-lro-options"],
        armResourceFlattening: resolvedOptions["arm-resource-flattening"],
        emitCommonTypesSchema: resolvedOptions["emit-common-types-schema"],
    };
}
async function getAllServicesAtAllVersions(program, options) {
    const tcgcSdkContext = createTCGCContext(program, "@azure-tools/typespec-autorest");
    const services = listServices(program);
    if (services.length === 0) {
        services.push({ type: program.getGlobalNamespaceType() });
    }
    const serviceRecords = [];
    for (const service of services) {
        const originalProgram = program;
        const versions = buildVersionProjections(program, service.type).filter((v) => !options.version || options.version === v.version);
        if (versions.length === 0) {
            reportDiagnostic(program, { code: "no-matching-version-found", target: service.type });
        }
        if (versions.length === 1 && versions[0].version === undefined) {
            let projectedProgram;
            if (versions[0].projections.length > 0) {
                projectedProgram = program = projectProgram(originalProgram, versions[0].projections);
            }
            const projectedServiceNs = projectedProgram
                ? projectedProgram.projector.projectedTypes.get(service.type)
                : service.type;
            const projectedService = projectedServiceNs === program.getGlobalNamespaceType()
                ? { type: program.getGlobalNamespaceType() }
                : getService(program, projectedServiceNs);
            const context = {
                program,
                outputFile: resolveOutputFile(program, service, services.length > 1, options),
                service: projectedService,
                tcgcSdkContext,
            };
            const result = await getOpenAPIForService(context, options);
            serviceRecords.push({
                service,
                versioned: false,
                ...result,
            });
        }
        else {
            const serviceRecord = {
                service,
                versioned: true,
                versions: [],
            };
            serviceRecords.push(serviceRecord);
            for (const record of versions) {
                const projectedProgram = (program = projectProgram(originalProgram, record.projections));
                const projectedServiceNs = projectedProgram
                    ? projectedProgram.projector.projectedTypes.get(service.type)
                    : service.type;
                const projectedService = projectedServiceNs === program.getGlobalNamespaceType()
                    ? { type: program.getGlobalNamespaceType() }
                    : getService(program, projectedServiceNs);
                const context = {
                    program,
                    outputFile: resolveOutputFile(program, projectedService, services.length > 1, options, record.version),
                    service: projectedService,
                    version: record.version,
                    tcgcSdkContext,
                };
                const result = await getOpenAPIForService(context, options);
                serviceRecord.versions.push({
                    ...result,
                    service: projectedService,
                    version: record.version,
                });
            }
        }
    }
    return serviceRecords;
}
async function emitAllServiceAtAllVersions(program, options) {
    const services = await getAllServicesAtAllVersions(program, options);
    if (program.compilerOptions.noEmit || program.hasError()) {
        return;
    }
    for (const serviceRecord of services) {
        if (serviceRecord.versioned) {
            for (const documentRecord of serviceRecord.versions) {
                await emitOutput(program, documentRecord, options);
            }
        }
        else {
            await emitOutput(program, serviceRecord, options);
        }
    }
}
async function emitOutput(program, result, options) {
    const sortedDocument = sortOpenAPIDocument(result.document);
    // Write out the OpenAPI document to the output path
    await emitFile(program, {
        path: result.outputFile,
        content: prettierOutput(JSON.stringify(sortedDocument, null, 2)),
        newLine: options.newLine,
    });
    // Copy examples to the output directory
    if (result.operationExamples.length > 0) {
        const examplesPath = resolvePath(getDirectoryPath(result.outputFile), "examples");
        await program.host.mkdirp(examplesPath);
        for (const { examples } of result.operationExamples) {
            if (examples) {
                for (const { relativePath, file } of Object.values(examples)) {
                    await emitFile(program, {
                        path: resolvePath(examplesPath, relativePath),
                        content: file.text,
                        newLine: options.newLine,
                    });
                }
            }
        }
    }
}
function prettierOutput(output) {
    return output + "\n";
}
function resolveOutputFile(program, service, multipleServices, options, version) {
    const azureResourceProviderFolder = options.azureResourceProviderFolder;
    if (azureResourceProviderFolder) {
        const info = resolveInfo(program, service.type);
        version = version ?? info?.version ?? "0000-00-00";
    }
    const interpolated = interpolatePath(options.outputFile, {
        "azure-resource-provider-folder": azureResourceProviderFolder,
        "service-name": multipleServices || azureResourceProviderFolder
            ? getNamespaceFullName(service.type)
            : undefined,
        "version-status": azureResourceProviderFolder
            ? version?.includes("preview")
                ? "preview"
                : "stable"
            : undefined,
        version,
    });
    return resolvePath(options.outputDir, interpolated);
}

const $decorators = {
    Autorest: {
        example: $example,
        useRef: $useRef,
    },
};

var f1 = /*#__PURE__*/Object.freeze({
    __proto__: null,
    $decorators: $decorators,
    $lib: $lib
});

var f0 = /*#__PURE__*/Object.freeze({
    __proto__: null,
    $decorators: $decorators,
    $example: $example,
    $lib: $lib,
    $onEmit: $onEmit,
    $useRef: $useRef,
    getAllServicesAtAllVersions: getAllServicesAtAllVersions,
    getExamples: getExamples,
    getOpenAPIForService: getOpenAPIForService,
    getRef: getRef,
    namespace: namespace,
    resolveAutorestOptions: resolveAutorestOptions,
    sortOpenAPIDocument: sortOpenAPIDocument
});

const TypeSpecJSSources = {
"dist/src/index.js": f0,
"dist/src/tsp-index.js": f1,
};
const TypeSpecSources = {
  "package.json": "{\"name\":\"@azure-tools/typespec-autorest\",\"version\":\"0.50.0\",\"author\":\"Microsoft Corporation\",\"description\":\"TypeSpec library for emitting openapi from the TypeSpec REST protocol binding\",\"homepage\":\"https://azure.github.io/typespec-azure\",\"readme\":\"https://github.com/Azure/typespec-azure/blob/main/README.md\",\"license\":\"MIT\",\"repository\":{\"type\":\"git\",\"url\":\"git+https://github.com/Azure/typespec-azure.git\"},\"bugs\":{\"url\":\"https://github.com/Azure/typespec-azure/issues\"},\"keywords\":[\"typespec\",\"autorest\"],\"type\":\"module\",\"main\":\"dist/src/index.js\",\"tspMain\":\"lib/autorest.tsp\",\"exports\":{\".\":{\"types\":\"./dist/src/index.d.ts\",\"default\":\"./dist/src/index.js\"},\"./testing\":{\"types\":\"./dist/src/testing/index.d.ts\",\"default\":\"./dist/src/testing/index.js\"}},\"engines\":{\"node\":\">=18.0.0\"},\"scripts\":{\"clean\":\"rimraf ./dist ./temp\",\"build\":\"npm run gen-extern-signature && npm run regen-autorest-openapi-schema && tsc -p . && npm run lint-typespec-library\",\"watch\":\"tsc -p . --watch\",\"gen-extern-signature\":\"tspd --enable-experimental gen-extern-signature .\",\"lint-typespec-library\":\"tsp compile . --warn-as-error --import @typespec/library-linter --no-emit\",\"regen-autorest-openapi-schema\":\"tsp compile ./schema/autorest-openapi-schema.tsp --warn-as-error && node ./.scripts/schema-json-to-js.js\",\"test\":\"vitest run\",\"test:watch\":\"vitest -w\",\"test:ui\":\"vitest --ui\",\"test:ci\":\"vitest run --coverage --reporter=junit --reporter=default\",\"lint\":\"eslint .  --max-warnings=0\",\"lint:fix\":\"eslint . --fix \",\"regen-docs\":\"tspd doc .  --enable-experimental  --output-dir ../../website/src/content/docs/docs/emitters/typespec-autorest/reference\"},\"files\":[\"lib/*.tsp\",\"schema/dist/schema.js\",\"dist/**\",\"!dist/test/**\"],\"peerDependencies\":{\"@azure-tools/typespec-azure-core\":\"workspace:~\",\"@azure-tools/typespec-azure-resource-manager\":\"workspace:~\",\"@azure-tools/typespec-client-generator-core\":\"workspace:~\",\"@typespec/compiler\":\"workspace:~\",\"@typespec/http\":\"workspace:~\",\"@typespec/openapi\":\"workspace:~\",\"@typespec/rest\":\"workspace:~\",\"@typespec/versioning\":\"workspace:~\"},\"devDependencies\":{\"@azure-tools/typespec-azure-core\":\"workspace:~\",\"@azure-tools/typespec-azure-resource-manager\":\"workspace:~\",\"@azure-tools/typespec-client-generator-core\":\"workspace:~\",\"@types/node\":\"~22.7.9\",\"@typespec/compiler\":\"workspace:~\",\"@typespec/http\":\"workspace:~\",\"@typespec/json-schema\":\"workspace:~\",\"@typespec/library-linter\":\"workspace:~\",\"@typespec/openapi\":\"workspace:~\",\"@typespec/rest\":\"workspace:~\",\"@typespec/tspd\":\"workspace:~\",\"@typespec/versioning\":\"workspace:~\",\"@vitest/coverage-v8\":\"^2.1.5\",\"@vitest/ui\":\"^2.1.2\",\"c8\":\"^10.1.2\",\"change-case\":\"~5.4.4\",\"rimraf\":\"~6.0.1\",\"typescript\":\"~5.6.3\",\"vitest\":\"^2.1.5\"}}",
  "../../core/packages/compiler/lib/intrinsics.tsp": "import \"../dist/src/lib/intrinsic/tsp-index.js\";\nimport \"./prototypes.tsp\";\n\n// This file contains all the intrinsic types of typespec. Everything here will always be loaded\nnamespace TypeSpec;\n\n/**\n * Represent a byte array\n */\nscalar bytes;\n\n/**\n * A numeric type\n */\nscalar numeric;\n\n/**\n * A whole number. This represent any `integer` value possible.\n * It is commonly represented as `BigInteger` in some languages.\n */\nscalar integer extends numeric;\n\n/**\n * A number with decimal value\n */\nscalar float extends numeric;\n\n/**\n * A 64-bit integer. (`-9,223,372,036,854,775,808` to `9,223,372,036,854,775,807`)\n */\nscalar int64 extends integer;\n\n/**\n * A 32-bit integer. (`-2,147,483,648` to `2,147,483,647`)\n */\nscalar int32 extends int64;\n\n/**\n * A 16-bit integer. (`-32,768` to `32,767`)\n */\nscalar int16 extends int32;\n\n/**\n * A 8-bit integer. (`-128` to `127`)\n */\nscalar int8 extends int16;\n\n/**\n * A 64-bit unsigned integer (`0` to `18,446,744,073,709,551,615`)\n */\nscalar uint64 extends integer;\n\n/**\n * A 32-bit unsigned integer (`0` to `4,294,967,295`)\n */\nscalar uint32 extends uint64;\n\n/**\n * A 16-bit unsigned integer (`0` to `65,535`)\n */\nscalar uint16 extends uint32;\n\n/**\n * A 8-bit unsigned integer (`0` to `255`)\n */\nscalar uint8 extends uint16;\n\n/**\n * An integer that can be serialized to JSON (`−9007199254740991 (−(2^53 − 1))` to `9007199254740991 (2^53 − 1)` )\n */\nscalar safeint extends int64;\n\n/**\n * A 64 bit floating point number. (`±5.0 × 10^−324` to `±1.7 × 10^308`)\n */\nscalar float64 extends float;\n\n/**\n * A 32 bit floating point number. (`±1.5 x 10^−45` to `±3.4 x 10^38`)\n */\nscalar float32 extends float64;\n\n/**\n * A decimal number with any length and precision. This represent any `decimal` value possible.\n * It is commonly represented as `BigDecimal` in some languages.\n */\nscalar decimal extends numeric;\n\n/**\n * A 128-bit decimal number.\n */\nscalar decimal128 extends decimal;\n\n/**\n * A sequence of textual characters.\n */\nscalar string;\n\n/**\n * A date on a calendar without a time zone, e.g. \"April 10th\"\n */\nscalar plainDate {\n  /**\n   * Create a plain date from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = plainTime.fromISO(\"2024-05-06\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * A time on a clock without a time zone, e.g. \"3:00 am\"\n */\nscalar plainTime {\n  /**\n   * Create a plain time from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = plainTime.fromISO(\"12:34\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * An instant in coordinated universal time (UTC)\"\n */\nscalar utcDateTime {\n  /**\n   * Create a date from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = utcDateTime.fromISO(\"2024-05-06T12:20-12Z\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * A date and time in a particular time zone, e.g. \"April 10th at 3:00am in PST\"\n */\nscalar offsetDateTime {\n  /**\n   * Create a date from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = offsetDateTime.fromISO(\"2024-05-06T12:20-12-0700\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * A duration/time period. e.g 5s, 10h\n */\nscalar duration {\n  /**\n   * Create a duration from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = duration.fromISO(\"P1Y1D\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * Boolean with `true` and `false` values.\n */\nscalar boolean;\n\n/**\n * @dev Array model type, equivalent to `Element[]`\n * @template Element The type of the array elements\n */\n@indexer(integer, Element)\nmodel Array<Element> {}\n\n/**\n * @dev Model with string properties where all the properties have type `Property`\n * @template Element The type of the properties\n */\n@indexer(string, Element)\nmodel Record<Element> {}\n",
  "../../core/packages/compiler/lib/prototypes.tsp": "namespace TypeSpec.Prototypes;\n\nextern dec getter(target: unknown);\n\nnamespace Types {\n  interface ModelProperty {\n    @getter type(): unknown;\n  }\n\n  interface Operation {\n    @getter returnType(): unknown;\n    @getter parameters(): unknown;\n  }\n\n  interface Array<TElementType> {\n    @getter elementType(): TElementType;\n  }\n}\n",
  "../../core/packages/compiler/lib/std/main.tsp": "// TypeSpec standard library. Everything in here can be omitted by using `--nostdlib` cli flag or `nostdlib` in the config.\nimport \"./types.tsp\";\nimport \"./decorators.tsp\";\nimport \"./reflection.tsp\";\nimport \"./projected-names.tsp\";\nimport \"./visibility.tsp\";\n",
  "../../core/packages/compiler/lib/std/types.tsp": "namespace TypeSpec;\n\n/**\n * Represent a 32-bit unix timestamp datetime with 1s of granularity.\n * It measures time by the number of seconds that have elapsed since 00:00:00 UTC on 1 January 1970.\n */\n@encode(\"unixTimestamp\", int32)\nscalar unixTimestamp32 extends utcDateTime;\n\n/**\n * Represent a model\n */\n// Deprecated June 2023 sprint\n#deprecated \"object is deprecated. Please use {} for an empty model, `Record<unknown>` for a record with unknown property types, `unknown[]` for an array.\"\nmodel object {}\n\n/**\n * Represent a URL string as described by https://url.spec.whatwg.org/\n */\nscalar url extends string;\n\n/**\n * Represents a collection of optional properties.\n *\n * @template Source An object whose spread properties are all optional.\n */\n@doc(\"The template for adding optional properties.\")\n@withOptionalProperties\nmodel OptionalProperties<Source> {\n  ...Source;\n}\n\n/**\n * Represents a collection of updateable properties.\n *\n * @template Source An object whose spread properties are all updateable.\n */\n@doc(\"The template for adding updateable properties.\")\n@withUpdateableProperties\nmodel UpdateableProperties<Source> {\n  ...Source;\n}\n\n/**\n * Represents a collection of omitted properties.\n *\n * @template Source An object whose properties are spread.\n * @template Keys The property keys to omit.\n */\n@doc(\"The template for omitting properties.\")\n@withoutOmittedProperties(Keys)\nmodel OmitProperties<Source, Keys extends string> {\n  ...Source;\n}\n\n/**\n * Represents a collection of properties with only the specified keys included.\n *\n * @template Source An object whose properties are spread.\n * @template Keys The property keys to include.\n */\n@doc(\"The template for picking properties.\")\n@withPickedProperties(Keys)\nmodel PickProperties<Source, Keys extends string> {\n  ...Source;\n}\n\n/**\n * Represents a collection of properties with default values omitted.\n *\n * @template Source An object whose spread property defaults are all omitted.\n */\n@withoutDefaultValues\nmodel OmitDefaults<Source> {\n  ...Source;\n}\n\n/**\n * Applies a visibility setting to a collection of properties.\n *\n * @template Source An object whose properties are spread.\n * @template Visibility The visibility to apply to all properties.\n */\n@doc(\"The template for setting the default visibility of key properties.\")\n@withDefaultKeyVisibility(Visibility)\nmodel DefaultKeyVisibility<Source, Visibility extends valueof string> {\n  ...Source;\n}\n",
  "../../core/packages/compiler/lib/std/decorators.tsp": "import \"../../dist/src/lib/tsp-index.js\";\n\nusing TypeSpec.Reflection;\n\nnamespace TypeSpec;\n\n/**\n * Typically a short, single-line description.\n * @param summary Summary string.\n *\n * @example\n * ```typespec\n * @summary(\"This is a pet\")\n * model Pet {}\n * ```\n */\nextern dec summary(target: unknown, summary: valueof string);\n\n/**\n * Attach a documentation string.\n * @param doc Documentation string\n * @param formatArgs Record with key value pair that can be interpolated in the doc.\n *\n * @example\n * ```typespec\n * @doc(\"Represent a Pet available in the PetStore\")\n * model Pet {}\n * ```\n */\nextern dec doc(target: unknown, doc: valueof string, formatArgs?: {});\n\n/**\n * Attach a documentation string to describe the successful return types of an operation.\n * If an operation returns a union of success and errors it only describes the success. See `@errorsDoc` for error documentation.\n * @param doc Documentation string\n *\n * @example\n * ```typespec\n * @returnsDoc(\"Returns doc\")\n * op get(): Pet | NotFound;\n * ```\n */\nextern dec returnsDoc(target: Operation, doc: valueof string);\n\n/**\n * Attach a documentation string to describe the error return types of an operation.\n * If an operation returns a union of success and errors it only describes the errors. See `@returnsDoc` for success documentation.\n * @param doc Documentation string\n *\n * @example\n * ```typespec\n * @errorsDoc(\"Errors doc\")\n * op get(): Pet | NotFound;\n * ```\n */\nextern dec errorsDoc(target: Operation, doc: valueof string);\n\n/**\n * Mark this type as deprecated.\n *\n * NOTE: This decorator **should not** be used, use the `#deprecated` directive instead.\n *\n * @deprecated Use the `#deprecated` [directive](https://typespec.io/docs/language-basics/directives/#deprecated) instead.\n * @param message Deprecation message.\n *\n * @example\n *\n * Use the `#deprecated` directive instead:\n *\n * ```typespec\n * #deprecated \"Use ActionV2\"\n * op Action<Result>(): Result;\n * ```\n */\n#deprecated \"@deprecated decorator is deprecated. Use the `#deprecated` directive instead.\"\nextern dec deprecated(target: unknown, message: valueof string);\n\n/**\n * Service options.\n */\nmodel ServiceOptions {\n  /**\n   * Title of the service.\n   */\n  title?: string;\n\n  /**\n   * Version of the service.\n   */\n  version?: string;\n}\n\n/**\n * Mark this namespace as describing a service and configure service properties.\n * @param options Optional configuration for the service.\n *\n * @example\n * ```typespec\n * @service\n * namespace PetStore;\n * ```\n *\n * @example Setting service title\n * ```typespec\n * @service({title: \"Pet store\"})\n * namespace PetStore;\n * ```\n *\n * @example Setting service version\n * ```typespec\n * @service({version: \"1.0\"})\n * namespace PetStore;\n * ```\n */\nextern dec service(target: Namespace, options?: ServiceOptions);\n\n/**\n * Specify that this model is an error type. Operations return error types when the operation has failed.\n *\n * @example\n * ```typespec\n * @error\n * model PetStoreError {\n *   code: string;\n *   message: string;\n * }\n * ```\n */\nextern dec error(target: Model);\n\n/**\n * Specify a known data format hint for this string type. For example `uuid`, `uri`, etc.\n * This differs from the `@pattern` decorator which is meant to specify a regular expression while `@format` accepts a known format name.\n * The format names are open ended and are left to emitter to interpret.\n *\n * @param format format name.\n *\n * @example\n * ```typespec\n * @format(\"uuid\")\n * scalar uuid extends string;\n * ```\n */\nextern dec format(target: string | bytes | ModelProperty, format: valueof string);\n\n/**\n * Specify the the pattern this string should respect using simple regular expression syntax.\n * The following syntax is allowed: alternations (`|`), quantifiers (`?`, `*`, `+`, and `{ }`), wildcard (`.`), and grouping parentheses.\n * Advanced features like look-around, capture groups, and references are not supported.\n *\n * This decorator may optionally provide a custom validation _message_. Emitters may choose to use the message to provide\n * context when pattern validation fails. For the sake of consistency, the message should be a phrase that describes in\n * plain language what sort of content the pattern attempts to validate. For example, a complex regular expression that\n * validates a GUID string might have a message like \"Must be a valid GUID.\"\n *\n * @param pattern Regular expression.\n * @param validationMessage Optional validation message that may provide context when validation fails.\n *\n * @example\n * ```typespec\n * @pattern(\"[a-z]+\", \"Must be a string consisting of only lower case letters and of at least one character.\")\n * scalar LowerAlpha extends string;\n * ```\n */\nextern dec pattern(\n  target: string | bytes | ModelProperty,\n  pattern: valueof string,\n  validationMessage?: valueof string\n);\n\n/**\n * Specify the minimum length this string type should be.\n * @param value Minimum length\n *\n * @example\n * ```typespec\n * @minLength(2)\n * scalar Username extends string;\n * ```\n */\nextern dec minLength(target: string | ModelProperty, value: valueof integer);\n\n/**\n * Specify the maximum length this string type should be.\n * @param value Maximum length\n *\n * @example\n * ```typespec\n * @maxLength(20)\n * scalar Username extends string;\n * ```\n */\nextern dec maxLength(target: string | ModelProperty, value: valueof integer);\n\n/**\n * Specify the minimum number of items this array should have.\n * @param value Minimum number\n *\n * @example\n * ```typespec\n * @minItems(1)\n * model Endpoints is string[];\n * ```\n */\nextern dec minItems(target: unknown[] | ModelProperty, value: valueof integer);\n\n/**\n * Specify the maximum number of items this array should have.\n * @param value Maximum number\n *\n * @example\n * ```typespec\n * @maxItems(5)\n * model Endpoints is string[];\n * ```\n */\nextern dec maxItems(target: unknown[] | ModelProperty, value: valueof integer);\n\n/**\n * Specify the minimum value this numeric type should be.\n * @param value Minimum value\n *\n * @example\n * ```typespec\n * @minValue(18)\n * scalar Age is int32;\n * ```\n */\nextern dec minValue(target: numeric | ModelProperty, value: valueof numeric);\n\n/**\n * Specify the maximum value this numeric type should be.\n * @param value Maximum value\n *\n * @example\n * ```typespec\n * @maxValue(200)\n * scalar Age is int32;\n * ```\n */\nextern dec maxValue(target: numeric | ModelProperty, value: valueof numeric);\n\n/**\n * Specify the minimum value this numeric type should be, exclusive of the given\n * value.\n * @param value Minimum value\n *\n * @example\n * ```typespec\n * @minValueExclusive(0)\n * scalar distance is float64;\n * ```\n */\nextern dec minValueExclusive(target: numeric | ModelProperty, value: valueof numeric);\n\n/**\n * Specify the maximum value this numeric type should be, exclusive of the given\n * value.\n * @param value Maximum value\n *\n * @example\n * ```typespec\n * @maxValueExclusive(50)\n * scalar distance is float64;\n * ```\n */\nextern dec maxValueExclusive(target: numeric | ModelProperty, value: valueof numeric);\n\n/**\n * Mark this string as a secret value that should be treated carefully to avoid exposure\n *\n * @example\n * ```typespec\n * @secret\n * scalar Password is string;\n * ```\n */\nextern dec secret(target: string | ModelProperty);\n\n/**\n * Attaches a tag to an operation, interface, or namespace. Multiple `@tag` decorators can be specified to attach multiple tags to a TypeSpec element.\n * @param tag Tag value\n */\nextern dec tag(target: Namespace | Interface | Operation, tag: valueof string);\n\n/**\n * Specifies how a templated type should name their instances.\n * @param name name the template instance should take\n * @param formatArgs Model with key value used to interpolate the name\n *\n * @example\n * ```typespec\n * @friendlyName(\"{name}List\", T)\n * model List<Item> {\n *   value: Item[];\n *   nextLink: string;\n * }\n * ```\n */\nextern dec friendlyName(target: unknown, name: valueof string, formatArgs?: unknown);\n\n/**\n * Provide a set of known values to a string type.\n * @param values Known values enum.\n *\n * @example\n * ```typespec\n * @knownValues(KnownErrorCode)\n * scalar ErrorCode extends string;\n *\n * enum KnownErrorCode {\n *   NotFound,\n *   Invalid,\n * }\n * ```\n */\n#deprecated \"This decorator has been deprecated. Use a named union of string literals with a string variant to achieve the same result without a decorator.\"\nextern dec knownValues(target: string | numeric | ModelProperty, values: Enum);\n\n/**\n * Mark a model property as the key to identify instances of that type\n * @param altName Name of the property. If not specified, the decorated property name is used.\n *\n * @example\n * ```typespec\n * model Pet {\n *   @key id: string;\n * }\n * ```\n */\nextern dec key(target: ModelProperty, altName?: valueof string);\n\n/**\n * Specify this operation is an overload of the given operation.\n * @param overloadbase Base operation that should be a union of all overloads\n *\n * @example\n * ```typespec\n * op upload(data: string | bytes, @header contentType: \"text/plain\" | \"application/octet-stream\"): void;\n * @overload(upload)\n * op uploadString(data: string, @header contentType: \"text/plain\" ): void;\n * @overload(upload)\n * op uploadBytes(data: bytes, @header contentType: \"application/octet-stream\"): void;\n * ```\n */\nextern dec overload(target: Operation, overloadbase: Operation);\n\n/**\n * DEPRECATED: Use `@encodedName` instead.\n *\n * Provide an alternative name for this type.\n * @param targetName Projection target\n * @param projectedName Alternative name\n *\n * @example\n * ```typespec\n * model Certificate {\n *   @projectedName(\"json\", \"exp\")\n *   expireAt: int32;\n * }\n * ```\n */\n#deprecated \"Use `@encodedName` instead for changing the name over the wire.\"\nextern dec projectedName(\n  target: unknown,\n  targetName: valueof string,\n  projectedName: valueof string\n);\n\n/**\n * Provide an alternative name for this type when serialized to the given mime type.\n * @param mimeType Mime type this should apply to. The mime type should be a known mime type as described here https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types without any suffix (e.g. `+json`)\n * @param name Alternative name\n *\n * @example\n *\n * ```typespec\n * model Certificate {\n *   @encodedName(\"application/json\", \"exp\")\n *   @encodedName(\"application/xml\", \"expiry\")\n *   expireAt: int32;\n * }\n * ```\n *\n * @example Invalid values\n *\n * ```typespec\n * @encodedName(\"application/merge-patch+json\", \"exp\")\n *              ^ error cannot use subtype\n * ```\n */\nextern dec encodedName(target: unknown, mimeType: valueof string, name: valueof string);\n\n/**\n * Specify the property to be used to discriminate this type.\n * @param propertyName The property name to use for discrimination\n *\n * @example\n *\n * ```typespec\n * @discriminator(\"kind\")\n * union Pet{ cat: Cat, dog: Dog }\n *\n * model Cat {kind: \"cat\", meow: boolean}\n * model Dog {kind: \"dog\", bark: boolean}\n * ```\n *\n * ```typespec\n * @discriminator(\"kind\")\n * model Pet{ kind: string }\n *\n * model Cat extends Pet {kind: \"cat\", meow: boolean}\n * model Dog extends Pet  {kind: \"dog\", bark: boolean}\n * ```\n */\nextern dec discriminator(target: Model | Union, propertyName: valueof string);\n\n/**\n * Known encoding to use on utcDateTime or offsetDateTime\n */\nenum DateTimeKnownEncoding {\n  /**\n   * RFC 3339 standard. https://www.ietf.org/rfc/rfc3339.txt\n   * Encode to string.\n   */\n  rfc3339: \"rfc3339\",\n\n  /**\n   * RFC 7231 standard. https://www.ietf.org/rfc/rfc7231.txt\n   * Encode to string.\n   */\n  rfc7231: \"rfc7231\",\n\n  /**\n   * Encode a datetime to a unix timestamp.\n   * Unix timestamps are represented as an integer number of seconds since the Unix epoch and usually encoded as an int32.\n   */\n  unixTimestamp: \"unixTimestamp\",\n}\n\n/**\n * Known encoding to use on duration\n */\nenum DurationKnownEncoding {\n  /**\n   * ISO8601 duration\n   */\n  ISO8601: \"ISO8601\",\n\n  /**\n   * Encode to integer or float\n   */\n  seconds: \"seconds\",\n}\n\n/**\n * Known encoding to use on bytes\n */\nenum BytesKnownEncoding {\n  /**\n   * Encode to Base64\n   */\n  base64: \"base64\",\n\n  /**\n   * Encode to Base64 Url\n   */\n  base64url: \"base64url\",\n}\n\n/**\n * Encoding for serializing arrays\n */\nenum ArrayEncoding {\n  /** Each values of the array is separated by a | */\n  pipeDelimited,\n\n  /** Each values of the array is separated by a <space> */\n  spaceDelimited,\n}\n\n/**\n * Specify how to encode the target type.\n * @param encodingOrEncodeAs Known name of an encoding or a scalar type to encode as(Only for numeric types to encode as string).\n * @param encodedAs What target type is this being encoded as. Default to string.\n *\n * @example offsetDateTime encoded with rfc7231\n *\n * ```tsp\n * @encode(\"rfc7231\")\n * scalar myDateTime extends offsetDateTime;\n * ```\n *\n * @example utcDateTime encoded with unixTimestamp\n *\n * ```tsp\n * @encode(\"unixTimestamp\", int32)\n * scalar myDateTime extends unixTimestamp;\n * ```\n *\n * @example encode numeric type to string\n *\n * ```tsp\n * model Pet {\n *   @encode(string) id: int64;\n * }\n * ```\n */\nextern dec encode(\n  target: Scalar | ModelProperty,\n  encodingOrEncodeAs: (valueof string | EnumMember) | Scalar,\n  encodedAs?: Scalar\n);\n\n/** Options for example decorators */\nmodel ExampleOptions {\n  /** The title of the example */\n  title?: string;\n\n  /** Description of the example */\n  description?: string;\n}\n\n/**\n * Provide an example value for a data type.\n *\n * @param example Example value.\n * @param options Optional metadata for the example.\n *\n * @example\n *\n * ```tsp\n * @example(#{name: \"Fluffy\", age: 2})\n * model Pet {\n *  name: string;\n *  age: int32;\n * }\n * ```\n */\nextern dec example(\n  target: Model | Enum | Scalar | Union | ModelProperty | UnionVariant,\n  example: valueof unknown,\n  options?: valueof ExampleOptions\n);\n\n/**\n * Operation example configuration.\n */\nmodel OperationExample {\n  /** Example request body. */\n  parameters?: unknown;\n\n  /** Example response body. */\n  returnType?: unknown;\n}\n\n/**\n * Provide example values for an operation's parameters and corresponding return type.\n *\n * @param example Example value.\n * @param options Optional metadata for the example.\n *\n * @example\n *\n * ```tsp\n * @opExample(#{parameters: #{name: \"Fluffy\", age: 2}, returnType: #{name: \"Fluffy\", age: 2, id: \"abc\"})\n * op createPet(pet: Pet): Pet;\n * ```\n */\nextern dec opExample(\n  target: Operation,\n  example: valueof OperationExample,\n  options?: valueof ExampleOptions\n);\n\n/**\n * Returns the model with required properties removed.\n */\nextern dec withOptionalProperties(target: Model);\n\n/**\n * Returns the model with any default values removed.\n */\nextern dec withoutDefaultValues(target: Model);\n\n/**\n * Returns the model with the given properties omitted.\n * @param omit List of properties to omit\n */\nextern dec withoutOmittedProperties(target: Model, omit: string | Union);\n\n/**\n * Returns the model with only the given properties included.\n * @param pick List of properties to include\n */\nextern dec withPickedProperties(target: Model, pick: string | Union);\n\n//---------------------------------------------------------------------------\n// Paging\n//---------------------------------------------------------------------------\n\n/**\n * Mark this operation as a `list` operation that returns a paginated list of items.\n */\nextern dec list(target: Operation);\n\n/**\n * Pagination property defining the number of items to skip.\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n * }\n * @list op listPets(@offset skip: int32, @pageSize pageSize: int8): Page<Pet>;\n * ```\n */\nextern dec offset(target: ModelProperty);\n\n/**\n * Pagination property defining the page index.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n * }\n * @list op listPets(@pageIndex page: int32, @pageSize pageSize: int8): Page<Pet>;\n * ```\n */\nextern dec pageIndex(target: ModelProperty);\n\n/**\n * Specify the pagination parameter that controls the maximum number of items to include in a page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n * }\n * @list op listPets(@pageIndex page: int32, @pageSize pageSize: int8): Page<Pet>;\n * ```\n */\nextern dec pageSize(target: ModelProperty);\n\n/**\n * Specify the the property that contains the array of page items.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n * }\n * @list op listPets(@pageIndex page: int32, @pageSize pageSize: int8): Page<Pet>;\n * ```\n */\nextern dec pageItems(target: ModelProperty);\n\n/**\n * Pagination property defining the token to get to the next page.\n * It MUST be specified both on the request parameter and the response.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @continuationToken continuationToken: string;\n * }\n * @list op listPets(@continuationToken continuationToken: string): Page<Pet>;\n * ```\n */\nextern dec continuationToken(target: ModelProperty);\n\n/**\n * Pagination property defining a link to the next page.\n *\n * It is expected that navigating to the link will return the same set of responses as the operation that returned the current page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @nextLink next: url;\n *   @prevLink prev: url;\n *   @firstLink first: url;\n *   @lastLink last: url;\n * }\n * @list op listPets(): Page<Pet>;\n * ```\n */\nextern dec nextLink(target: ModelProperty);\n\n/**\n * Pagination property defining a link to the previous page.\n *\n * It is expected that navigating to the link will return the same set of responses as the operation that returned the current page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @nextLink next: url;\n *   @prevLink prev: url;\n *   @firstLink first: url;\n *   @lastLink last: url;\n * }\n * @list op listPets(): Page<Pet>;\n * ```\n */\nextern dec prevLink(target: ModelProperty);\n\n/**\n * Pagination property defining a link to the first page.\n *\n * It is expected that navigating to the link will return the same set of responses as the operation that returned the current page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @nextLink next: url;\n *   @prevLink prev: url;\n *   @firstLink first: url;\n *   @lastLink last: url;\n * }\n * @list op listPets(): Page<Pet>;\n * ```\n */\nextern dec firstLink(target: ModelProperty);\n\n/**\n * Pagination property defining a link to the last page.\n *\n * It is expected that navigating to the link will return the same set of responses as the operation that returned the current page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @nextLink next: url;\n *   @prevLink prev: url;\n *   @firstLink first: url;\n *   @lastLink last: url;\n * }\n * @list op listPets(): Page<Pet>;\n * ```\n */\nextern dec lastLink(target: ModelProperty);\n\n//---------------------------------------------------------------------------\n// Debugging\n//---------------------------------------------------------------------------\n\n/**\n * A debugging decorator used to inspect a type.\n * @param text Custom text to log\n */\nextern dec inspectType(target: unknown, text: valueof string);\n\n/**\n * A debugging decorator used to inspect a type name.\n * @param text Custom text to log\n */\nextern dec inspectTypeName(target: unknown, text: valueof string);\n",
  "../../core/packages/compiler/lib/std/reflection.tsp": "namespace TypeSpec.Reflection;\n\nmodel Enum {}\nmodel EnumMember {}\nmodel Interface {}\nmodel Model {}\nmodel ModelProperty {}\nmodel Namespace {}\nmodel Operation {}\nmodel Scalar {}\nmodel Union {}\nmodel UnionVariant {}\nmodel StringTemplate {}\n",
  "../../core/packages/compiler/lib/std/projected-names.tsp": "// Set of projections consuming the @projectedName decorator\n#suppress \"projections-are-experimental\"\nprojection op#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n  }\n}\n\n#suppress \"projections-are-experimental\"\nprojection interface#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n  }\n}\n\n#suppress \"projections-are-experimental\"\nprojection model#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n\n    self::properties::forEach((p) => {\n      if hasProjectedName(p, targetName) {\n        self::renameProperty(p::name, getProjectedName(p, targetName));\n      };\n    });\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n\n    self::projectionBase::properties::forEach((p) => {\n      if hasProjectedName(p, targetName) {\n        self::renameProperty(getProjectedName(p, targetName), p::name);\n      };\n    });\n  }\n}\n\n#suppress \"projections-are-experimental\"\nprojection enum#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n\n    self::members::forEach((p) => {\n      if hasProjectedName(p, targetName) {\n        self::renameMember(p::name, getProjectedName(p, targetName));\n      };\n    });\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n\n    self::projectionBase::members::forEach((p) => {\n      if hasProjectedName(p, targetName) {\n        self::renameMember(getProjectedName(p, targetName), p::name);\n      };\n    });\n  }\n}\n\n#suppress \"projections-are-experimental\"\nprojection union#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n  }\n}\n",
  "../../core/packages/compiler/lib/std/visibility.tsp": "// Copyright (c) Microsoft Corporation\n// Licensed under the MIT license.\n\nimport \"../../dist/src/lib/tsp-index.js\";\n\nusing TypeSpec.Reflection;\n\nnamespace TypeSpec;\n\n/**\n * Indicates that a property is only considered to be present or applicable (\"visible\") with\n * the in the given named contexts (\"visibilities\"). When a property has no visibilities applied\n * to it, it is implicitly visible always.\n *\n * As far as the TypeSpec core library is concerned, visibilities are open-ended and can be arbitrary\n * strings, but  the following visibilities are well-known to standard libraries and should be used\n * with standard emitters that interpret them as follows:\n *\n * - \"read\": output of any operation.\n * - \"create\": input to operations that create an entity..\n * - \"query\": input to operations that read data.\n * - \"update\": input to operations that update data.\n * - \"delete\": input to operations that delete data.\n *\n * See also: [Automatic visibility](https://typespec.io/docs/libraries/http/operations#automatic-visibility)\n *\n * @param visibilities List of visibilities which apply to this property.\n *\n * @example\n *\n * ```typespec\n * model Dog {\n *   // the service will generate an ID, so you don't need to send it.\n *   @visibility(Lifecycle.Read) id: int32;\n *   // the service will store this secret name, but won't ever return it\n *   @visibility(Lifecycle.Create, Lifecycle.Update) secretName: string;\n *   // the regular name is always present\n *   name: string;\n * }\n * ```\n */\nextern dec visibility(target: ModelProperty, ...visibilities: valueof (string | EnumMember)[]);\n\n/**\n * Indicates that a property is not visible in the given visibility class.\n *\n * This decorator removes all active visibility modifiers from the property within\n * the given visibility class.\n *\n * @param visibilityClass The visibility class to make the property invisible within.\n *\n * @example\n * ```typespec\n * model Example {\n *   @invisible(Lifecycle)\n *   hidden_property: string;\n * }\n * ```\n */\nextern dec invisible(target: ModelProperty, visibilityClass: Enum);\n\n/**\n * Removes visibility modifiers from a property.\n *\n * If the visibility modifiers for a visibility class have not been initialized,\n * this decorator will use the default visibility modifiers for the visibility\n * class as the default modifier set.\n *\n * @param target The property to remove visibility from.\n * @param visibilities The visibility modifiers to remove from the target property.\n *\n * @example\n * ```typespec\n * model Example {\n *   // This property will have the Create and Update visibilities, but not the\n *   // Read visibility, since it is removed.\n *   @removeVisibility(Lifecycle.Read)\n *   secret_property: string;\n * }\n * ```\n */\nextern dec removeVisibility(target: ModelProperty, ...visibilities: valueof EnumMember[]);\n\n/**\n * Removes properties that are not considered to be present or applicable\n * (\"visible\") in the given named contexts (\"visibilities\"). Can be used\n * together with spread to effectively spread only visible properties into\n * a new model.\n *\n * See also: [Automatic visibility](https://typespec.io/docs/libraries/http/operations#automatic-visibility)\n *\n * When using an emitter that applies visibility automatically, it is generally\n * not necessary to use this decorator.\n *\n * @param visibilities List of visibilities which apply to this property.\n *\n * @example\n * ```typespec\n * model Dog {\n *   @visibility(\"read\") id: int32;\n *   @visibility(\"create\", \"update\") secretName: string;\n *   name: string;\n * }\n *\n * // The spread operator will copy all the properties of Dog into DogRead,\n * // and @withVisibility will then remove those that are not visible with\n * // create or update visibility.\n * //\n * // In this case, the id property is removed, and the name and secretName\n * // properties are kept.\n * @withVisibility(\"create\", \"update\")\n * model DogCreateOrUpdate {\n *   ...Dog;\n * }\n *\n * // In this case the id and name properties are kept and the secretName property\n * // is removed.\n * @withVisibility(\"read\")\n * model DogRead {\n *   ...Dog;\n * }\n * ```\n */\nextern dec withVisibility(target: Model, ...visibilities: valueof (string | EnumMember)[]);\n\n/**\n * Set the visibility of key properties in a model if not already set.\n *\n * This will set the visibility modifiers of all key properties in the model if the visibility is not already _explicitly_ set,\n * but will not change the visibility of any properties that have visibility set _explicitly_, even if the visibility\n * is the same as the default visibility.\n *\n * Visibility may be explicitly set using any of the following decorators:\n *\n * - `@visibility`\n * - `@removeVisibility`\n * - `@invisible`\n *\n * @param visibility The desired default visibility value. If a key property already has visibility set, it will not be changed.\n */\nextern dec withDefaultKeyVisibility(target: Model, visibility: valueof string | EnumMember);\n\n/**\n * Sets which visibilities apply to parameters for the given operation.\n *\n * @param visibilities List of visibility strings which apply to this operation.\n */\nextern dec parameterVisibility(target: Operation, ...visibilities: valueof (string | EnumMember)[]);\n\n/**\n * Sets which visibilities apply to the return type for the given operation.\n * @param visibilities List of visibility strings which apply to this operation.\n */\nextern dec returnTypeVisibility(\n  target: Operation,\n  ...visibilities: valueof (string | EnumMember)[]\n);\n\n/**\n * Returns the model with non-updateable properties removed.\n */\nextern dec withUpdateableProperties(target: Model);\n\n/**\n * Declares the default visibility modifiers for a visibility class.\n *\n * The default modifiers are used when a property does not have any visibility decorators\n * applied to it.\n *\n * The modifiers passed to this decorator _MUST_ be members of the target Enum.\n *\n * @param visibilities the list of modifiers to use as the default visibility modifiers.\n */\nextern dec defaultVisibility(target: Enum, ...visibilities: valueof EnumMember[]);\n\n/**\n * A visibility class for resource lifecycle phases.\n *\n * These visibilities control whether a property is visible during the create, read, and update phases of a resource's\n * lifecycle.\n *\n * @example\n * ```typespec\n * model Dog {\n *  @visibility(Lifecycle.Read) id: int32;\n *  @visibility(Lifecycle.Create, Lifecycle.Update) secretName: string;\n *  name: string;\n * }\n * ```\n *\n * In this example, the `id` property is only visible during the read phase, and the `secretName` property is only visible\n * during the create and update phases. This means that the server will return the `id` property when returning a `Dog`,\n * but the client will not be able to set or update it. In contrast, the `secretName` property can be set when creating\n * or updating a `Dog`, but the server will never return it. The `name` property has no visibility modifiers and is\n * therefore visible in all phases.\n */\nenum Lifecycle {\n  Create,\n  Read,\n  Update,\n}\n\n/**\n * A visibility filter, used to specify which properties should be included when\n * using the `withVisibilityFilter` decorator.\n *\n * The filter matches any property with ALL of the following:\n * - If the `any` key is present, the property must have at least one of the specified visibilities.\n * - If the `all` key is present, the property must have all of the specified visibilities.\n * - If the `none` key is present, the property must have none of the specified visibilities.\n */\nmodel VisibilityFilter {\n  any?: EnumMember[];\n  all?: EnumMember[];\n  none?: EnumMember[];\n}\n\n/**\n * Applies the given visibility filter to the properties of the target model.\n *\n * This transformation is recursive, so it will also apply the filter to any nested\n * or referenced models that are the types of any properties in the `target`.\n *\n * @param target The model to apply the visibility filter to.\n * @param filter The visibility filter to apply to the properties of the target model.\n *\n * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * @withVisibilityFilter(#{ all: #[Lifecycle.Read] })\n * model DogRead {\n *  ...Dog\n * }\n * ```\n */\nextern dec withVisibilityFilter(target: Model, filter: valueof VisibilityFilter);\n\n/**\n * Transforms the `target` model to include only properties that are visible during the\n * \"Update\" lifecycle phase.\n *\n * Any nested models of optional properties will be transformed into the \"CreateOrUpdate\"\n * lifecycle phase instead of the \"Update\" lifecycle phase, so that nested models may be\n * fully updated.\n *\n * @param target The model to apply the transformation to.\n *\n * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   @visibility(Lifecycle.Create, Lifecycle.Update)\n *   secretName: string;\n *\n *   name: string;\n * }\n *\n * @withLifecycleUpdate\n * model DogUpdate {\n *   ...Dog\n * }\n * ```\n */\nextern dec withLifecycleUpdate(target: Model);\n\n/**\n * A copy of the input model `T` with only the properties that are visible during the\n * \"Create\" resource lifecycle phase.\n *\n * This transformation is recursive, and will include only properties that have the\n * `Lifecycle.Create` visibility modifier.\n *\n * If a `NameTemplate` is provided, the new model will be named according to the template.\n * The template uses the same syntax as the `@friendlyName` decorator.\n *\n * @template T The model to transform.\n * @template NameTemplate The name template to use for the new model.\n *\n *  * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * model CreateDog is Create<Dog>;\n * ```\n */\n@friendlyName(NameTemplate, T)\n@withVisibilityFilter(#{ all: #[Lifecycle.Create] })\nmodel Create<T extends Reflection.Model, NameTemplate extends valueof string = \"Create{name}\"> {\n  ...T;\n}\n\n/**\n * A copy of the input model `T` with only the properties that are visible during the\n * \"Read\" resource lifecycle phase.\n *\n * This transformation is recursive, and will include only properties that have the\n * `Lifecycle.Read` visibility modifier.\n *\n * If a `NameTemplate` is provided, the new model will be named according to the template.\n * The template uses the same syntax as the `@friendlyName` decorator.\n *\n * @template T The model to transform.\n * @template NameTemplate The name template to use for the new model.\n *\n *  * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * model ReadDog is Read<Dog>;\n * ```\n */\n@friendlyName(NameTemplate, T)\n@withVisibilityFilter(#{ all: #[Lifecycle.Read] })\nmodel Read<T extends Reflection.Model, NameTemplate extends valueof string = \"Read{name}\"> {\n  ...T;\n}\n\n/**\n * A copy of the input model `T` with only the properties that are visible during the\n * \"Update\" resource lifecycle phase.\n *\n * This transformation will include only the properties that have the `Lifecycle.Update`\n * visibility modifier, and the types of all properties will be replaced with the\n * equivalent `CreateOrUpdate` transformation.\n *\n * If a `NameTemplate` is provided, the new model will be named according to the template.\n * The template uses the same syntax as the `@friendlyName` decorator.\n *\n * @template T The model to transform.\n * @template NameTemplate The name template to use for the new model.\n *\n *  * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * model UpdateDog is Update<Dog>;\n * ```\n */\n@friendlyName(NameTemplate, T)\n@withLifecycleUpdate\nmodel Update<T extends Reflection.Model, NameTemplate extends valueof string = \"Update{name}\"> {\n  ...T;\n}\n\n/**\n * A copy of the input model `T` with only the properties that are visible during the\n * \"Create\" or \"Update\" resource lifecycle phases.\n *\n * This transformation is recursive, and will include only properties that have the\n * `Lifecycle.Create` or `Lifecycle.Update` visibility modifier.\n *\n * If a `NameTemplate` is provided, the new model will be named according to the template.\n * The template uses the same syntax as the `@friendlyName` decorator.\n *\n * @template T The model to transform.\n * @template NameTemplate The name template to use for the new model.\n *\n *  * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * model CreateOrUpdateDog is CreateOrUpdate<Dog>;\n * ```\n */\n@friendlyName(NameTemplate, T)\n@withVisibilityFilter(#{ any: #[Lifecycle.Create, Lifecycle.Update] })\nmodel CreateOrUpdate<\n  T extends Reflection.Model,\n  NameTemplate extends valueof string = \"CreateOrUpdate{name}\"\n> {\n  ...T;\n}\n",
  "lib/autorest.tsp": "import \"./decorators.tsp\";\nimport \"../dist/src/tsp-index.js\";\n",
  "lib/decorators.tsp": "using TypeSpec.Reflection;\n\nnamespace Autorest;\n\n/**\n * `@example` - attaches example files to an operation. Multiple examples can be specified.\n *\n * `@example` can be specified on Operations.\n *\n * @param pathOrUri - path or Uri to the example file.\n * @param title - name or description of the example file.\n */\nextern dec example(target: Operation, pathOrUri: valueof string, title: valueof string);\n\n/**\n * `@useRef` - is used to replace the TypeSpec model type in emitter output with a pre-existing named OpenAPI schema such as Azure Resource Manager common types.\n *\n * `@useRef` can be specified on Models and ModelProperty.\n *\n * @param jsonRef - path or Uri to an OpenAPI schema.\n */\nextern dec useRef(entity: Model | ModelProperty, jsonRef: valueof string);\n"
};
const _TypeSpecLibrary_ = {
  jsSourceFiles: TypeSpecJSSources,
  typespecSourceFiles: TypeSpecSources,
};

export { $decorators, $example, $lib, $onEmit, $useRef, _TypeSpecLibrary_, getAllServicesAtAllVersions, getExamples, getOpenAPIForService, getRef, namespace, resolveAutorestOptions, sortOpenAPIDocument };
