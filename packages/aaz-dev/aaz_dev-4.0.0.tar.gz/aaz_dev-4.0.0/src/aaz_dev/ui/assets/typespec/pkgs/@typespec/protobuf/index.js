import { createTypeSpecLibrary, paramMessage, resolvePath, getDoc, isDeclaredInNamespace, getEffectiveModelType, formatDiagnostic, getFriendlyName, isTemplateInstance, SyntaxKind, compilerAssert, isType, getTypeName } from '@typespec/compiler';

// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.
const EmitterOptionsSchema = {
    type: "object",
    additionalProperties: false,
    properties: {
        noEmit: {
            type: "boolean",
            nullable: true,
            description: "If set to `true`, this emitter will not write any files. It will still validate the TypeSpec sources to ensure they are compatible with Protobuf, but the files will simply not be written to the output directory.",
        },
        "omit-unreachable-types": {
            type: "boolean",
            nullable: true,
            description: "By default, the emitter will create `message` declarations for any models in a namespace decorated with `@package` that have an `@field` decorator on every property. If this option is set to true, this behavior will be disabled, and only messages that are explicitly decorated with `@message` or that are reachable from a service operation will be emitted.",
        },
    },
    required: [],
};
const PACKAGE_NAME = "@typespec/protobuf";
const TypeSpecProtobufLibrary = createTypeSpecLibrary({
    name: PACKAGE_NAME,
    requireImports: [PACKAGE_NAME],
    diagnostics: {
        "field-index": {
            severity: "error",
            messages: {
                missing: paramMessage `field ${"name"} does not have a field index, but one is required (try using the '@field' decorator)`,
                invalid: paramMessage `field index ${"index"} is invalid (must be an integer greater than zero)`,
                "out-of-bounds": paramMessage `field index ${"index"} is out of bounds (must be less than ${"max"})`,
                reserved: paramMessage `field index ${"index"} falls within the implementation-reserved range of 19000-19999 inclusive`,
                "user-reserved": paramMessage `field index ${"index"} was reserved by a call to @reserve on this model`,
                "user-reserved-range": paramMessage `field index ${"index"} falls within a range reserved by a call to @reserve on this model`,
            },
        },
        "field-name": {
            severity: "error",
            messages: {
                "user-reserved": paramMessage `field name '${"name"}' was reserved by a call to @reserve on this model`,
            },
        },
        "root-operation": {
            severity: "error",
            messages: {
                default: "operations in the root namespace are not supported (no associated Protobuf service)",
            },
        },
        "unsupported-intrinsic": {
            severity: "error",
            messages: {
                default: paramMessage `intrinsic type ${"name"} is not supported in Protobuf`,
            },
        },
        "unsupported-return-type": {
            severity: "error",
            messages: {
                default: "Protobuf methods must return a named Model",
            },
        },
        "unsupported-input-type": {
            severity: "error",
            messages: {
                "wrong-number": "Protobuf methods must accept exactly one Model input (an empty model will do)",
                "wrong-type": "Protobuf methods may only accept a named Model as an input",
                unconvertible: "input parameters cannot be converted to a Protobuf message",
            },
        },
        "unsupported-field-type": {
            severity: "error",
            messages: {
                unconvertible: paramMessage `cannot convert a ${"type"} to a protobuf type (only intrinsic types and models are supported)`,
                "unknown-intrinsic": paramMessage `no known protobuf scalar for intrinsic type ${"name"}`,
                "unknown-scalar": paramMessage `no known protobuf scalar for TypeSpec scalar type ${"name"}`,
                "recursive-map": "a protobuf map's 'value' type may not refer to another map",
                union: "a message field's type may not be a union",
            },
        },
        "namespace-collision": {
            severity: "error",
            messages: {
                default: paramMessage `the package name ${"name"} has already been used`,
            },
        },
        "unconvertible-enum": {
            severity: "error",
            messages: {
                default: "enums must explicitly assign exactly one integer to each member to be used in a Protobuf message",
                "no-zero-first": "the first variant of an enum must be set to zero to be used in a Protobuf message",
            },
        },
        "nested-array": {
            severity: "error",
            messages: {
                default: "nested arrays are not supported by the Protobuf emitter",
            },
        },
        "invalid-package-name": {
            severity: "error",
            messages: {
                default: paramMessage `${"name"} is not a valid package name (must consist of letters and numbers separated by ".")`,
            },
        },
        "illegal-reservation": {
            severity: "error",
            messages: {
                default: "reservation value must be a string literal, uint32 literal, or a tuple of two uint32 literals denoting a range",
            },
        },
        "model-not-in-package": {
            severity: "error",
            messages: {
                default: paramMessage `model ${"name"} is not in a namespace that uses the '@Protobuf.package' decorator`,
            },
        },
        "anonymous-model": {
            severity: "error",
            messages: {
                default: "anonymous models cannot be used in Protobuf messages",
            },
        },
        "unspeakable-template-argument": {
            severity: "error",
            messages: {
                default: paramMessage `template ${"name"} cannot be converted to a Protobuf message because it has an unspeakable argument (try using the '@friendlyName' decorator on the template)`,
            },
        },
        package: {
            severity: "error",
            messages: {
                "disallowed-option-type": paramMessage `option '${"name"}' with type '${"type"}' is not allowed in a package declaration (only string, boolean, and numeric types are allowed)`,
            },
        },
    },
    emitter: { options: EmitterOptionsSchema },
});
const __DIAGNOSTIC_CACHE = new WeakMap();
function getDiagnosticCache(program) {
    let cache = __DIAGNOSTIC_CACHE.get(program);
    if (!cache) {
        cache = new Map();
        __DIAGNOSTIC_CACHE.set(program, cache);
    }
    return cache;
}
function getAppliedCodesForTarget(program, target) {
    const cache = getDiagnosticCache(program);
    let codes = cache.get(target);
    if (!codes) {
        codes = new Set();
        cache.set(target, codes);
    }
    return codes;
}
const reportDiagnostic = Object.assign(TypeSpecProtobufLibrary.reportDiagnostic, {
    /**
     * Report a TypeSpec protobuf diagnostic, but only once per target per diagnostic code.
     *
     * This is useful in situations where a function that reports a recoverable diagnostic may be called multiple times.
     */
    once: function (program, diagnostic) {
        const codes = getAppliedCodesForTarget(program, diagnostic.target);
        if (codes.has(diagnostic.code)) {
            return;
        }
        codes.add(diagnostic.code);
        TypeSpecProtobufLibrary.reportDiagnostic(program, diagnostic);
    },
});
const keys = [
    "fieldIndex",
    "package",
    "service",
    "externRef",
    "stream",
    "reserve",
    "message",
    "_map",
];
const state = Object.fromEntries(keys.map((k) => [k, TypeSpecProtobufLibrary.createStateSymbol(k)]));

// Copyright (c) Microsoft Corporation.
// Symbols for type destructuring
const $scalar = Symbol("$scalar");
const $ref = Symbol("$ref");
const $map = Symbol("$map");
/**
 * Create a scalar type by name.
 */
function scalar(t) {
    return [$scalar, t];
}
/**
 * Create a type reference (symbol) to a named message.
 */
function ref(t) {
    return [$ref, t];
}
/**
 * Create a map from a key type to a value type.
 */
function map(k, v) {
    return [$map, k, v];
}
/* c8 ignore start */
// Unreachable, by definition, should not be covered :)
/**
 * Creates a type that will throw an internal error if the system attempts to emit it.
 *
 * @param message - optional message that should be printed
 */
function unreachable(message = "tried to emit unreachable type") {
    // This little "array-like" object will throw an internal error as soon as the "tag" is inspected.
    return Object.freeze({
        get [0]() {
            throw new Error("Internal Error: " + message);
        },
    });
}
/**
 * A helper function that matches and delegates a Protobuf type to a handler per type.
 *
 * @param type - the Protobuf type to match and delegate
 * @param pattern - the matching pattern of delegates to apply
 * @returns
 */
function matchType(type, pattern) {
    switch (type[0]) {
        case $ref:
            return pattern.ref(type[1]);
        case $scalar:
            return pattern.scalar(type[1]);
        case $map:
            return pattern.map(type[1], type[2]);
        /* c8 ignore next 5 */
        default:
            const __exhaust = type[0];
            throw new Error(`Internal Error: unreachable matchType variant ${__exhaust}`);
    }
}

// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.
// This module defines how to emit the text representation of a ProtoFile AST.
const PROTO_MAX_ONE_LINE_DOC_LENGTH = 80;
/**
 * Write the given `file` to a string.
 */
function writeProtoFile(file) {
    let result = "// Generated by Microsoft TypeSpec\n";
    let docComment = collect(writeBlockDocumentationComment(file)).join("\n");
    if (docComment.length > 0)
        docComment = "\n" + docComment;
    result += docComment;
    result += '\nsyntax = "proto3";\n';
    if (file.package)
        result += `\npackage ${file.package};\n`;
    for (const _import of file.imports) {
        result += `\nimport "${_import}";`;
    }
    if (file.imports.length > 0)
        result += "\n";
    const opts = Object.entries(file.options);
    for (const [name, valueData] of opts) {
        const value = typeof valueData === "string" ? `"${valueData}"` : valueData.toString();
        result += `\noption ${name} = ${value};`;
    }
    // Give the declarations a little breathing room if options were provided
    if (opts.length > 0)
        result += "\n";
    for (const decl of file.declarations) {
        result += "\n" + collect(writeDeclaration(decl, 0)).join("\n") + "\n";
    }
    return result;
}
/**
 * Write the given `decl` to a line iterable.
 */
function* writeDeclaration(decl, indentLevel) {
    switch (decl.kind) {
        case "message":
            yield* writeMessage(decl, indentLevel);
            return;
        case "service":
            yield* writeService(decl, indentLevel);
            return;
        case "field":
            yield* writeField(decl, indentLevel);
            return;
        case "oneof":
            yield* writeOneOf(decl, indentLevel);
            return;
        case "enum":
            yield* writeEnum(decl, indentLevel);
            return;
        case "variant":
            yield* writeVariant(decl, indentLevel);
            return;
        case "method":
            yield* writeMethod(decl);
            return;
        /* c8 ignore next 5 */
        default:
            const __exhaust = decl;
            throw __exhaust;
    }
}
/**
 * Write the given message `decl` to a line iterable.
 */
function* writeMessage(decl, indentLevel) {
    yield* writeBlockDocumentationComment(decl);
    const head = `message ${decl.name} {`;
    const tail = "}";
    if (decl.declarations.length > 0 || decl.reservations?.length) {
        yield head;
        yield* indent(writeReservations(decl));
        yield* indent(flatMap(decl.declarations, (decl) => writeDeclaration(decl, indentLevel + 1)));
        yield tail;
    }
    else
        yield head + tail;
}
function* writeReservations(decl) {
    const { reservedNumbers, reservedNames } = selectMap(decl.reservations ?? [], (v) => (typeof v === "number" || Array.isArray(v) ? "reservedNumbers" : "reservedNames"), {
        reservedNumbers: (v) => (Array.isArray(v) ? v[0] + " to " + v[1] : v.toString()),
        reservedNames: (v) => `"${v.toString()}"`,
    });
    if (reservedNumbers.length + reservedNames.length > 0) {
        if (reservedNumbers.length > 0)
            yield `reserved ${reservedNumbers.join(", ")};`;
        if (reservedNames.length > 0)
            yield `reserved ${reservedNames.join(", ")};`;
        yield "";
    }
}
function* writeService(decl, indentLevel) {
    yield* writeBlockDocumentationComment(decl);
    const head = `service ${decl.name} {`;
    const tail = "}";
    if (decl.operations.length > 0) {
        yield head;
        yield* indent(flatMap(decl.operations, (decl) => writeDeclaration(decl, indentLevel + 1)));
        yield tail;
    }
    else
        yield head + tail;
}
function* writeMethod(decl) {
    yield* writeBlockDocumentationComment(decl);
    const [inStream, outStream] = [
        decl.stream & 2 /* StreamingMode.In */,
        decl.stream & 1 /* StreamingMode.Out */,
    ].map((v) => (v ? "stream " : ""));
    yield `rpc ${decl.name}(${inStream}${writeType(decl.input)}) returns (${outStream}${writeType(decl.returns)});`;
}
function* writeOneOf(decl, indentLevel) {
    yield* writeBlockDocumentationComment(decl);
    // OneOf declarations must have at least one element, so no need to check for declarations
    yield `oneof ${decl.name} {`;
    yield* indent(flatMap(decl.declarations, (decl) => writeDeclaration(decl, indentLevel + 1)));
    yield "}";
}
function* writeEnum(decl, indentLevel) {
    yield* writeBlockDocumentationComment(decl);
    yield `enum ${decl.name} {`;
    if (decl.allowAlias) {
        yield "  option allow_alias = true;";
        if (decl.variants.length > 0)
            yield "";
    }
    yield* indent(flatMap(decl.variants, (decl) => writeDeclaration(decl, indentLevel + 1)));
    yield "}";
}
function writeVariant(decl, indentLevel) {
    const output = `${decl.name} = ${decl.value};`;
    return writeDocumentationCommentFlexible(decl, output, indentLevel);
}
function writeField(decl, indentLevel) {
    const prefix = decl.repeated ? "repeated " : "";
    const output = prefix + `${writeType(decl.type)} ${decl.name} = ${decl.index};`;
    return writeDocumentationCommentFlexible(decl, output, indentLevel);
}
function writeType(type) {
    return matchType(type, {
        map: (k, v) => `map<${k}, ${writeType(v)}>`,
        ref: (r) => r,
        scalar: (s) => s,
    });
}
// #region utils
/**
 * Indents an iterable of strings by prepending an amount of spaces to each item
 * in the iterable.
 *
 * @param it - the string iterable to indent
 * @param depth - the indentation depth in spaces, defaults to 2
 */
function* indent(it, depth = 2) {
    for (const value of it) {
        if (value !== "") {
            yield " ".repeat(depth) + value;
        }
        else
            yield value;
    }
}
/**
 * Writes a block comment from the given declaration.
 */
function* writeBlockDocumentationComment(decl) {
    yield* decl.doc
        ?.trim()
        .split("\n")
        .map((line) => `// ${line}`) ?? [];
}
/**
 * Writes a block comment or inline postfix comment depending on the length of the content.
 */
function* writeDocumentationCommentFlexible(decl, output, indentLevel) {
    const docComment = decl.doc?.trim();
    const docCommentIsOneLine = docComment && !docComment?.includes("\n");
    const fullLength = indentLevel * 2 + output.length + 1 + (docComment?.length ?? 0);
    if (docCommentIsOneLine && fullLength <= PROTO_MAX_ONE_LINE_DOC_LENGTH) {
        yield output + " // " + decl.doc;
    }
    else {
        yield* writeBlockDocumentationComment(decl);
        yield output;
    }
}
/**
 * A version of flatMap that works with generic iterables.
 *
 * @param it - the iterable to flatten and map
 * @param f - the function to run on the items of `it`
 */
function* flatMap(it, f) {
    for (const value of it) {
        const result = f(value);
        if (typeof result === "object" && result !== null && Symbol.iterator in result) {
            yield* result;
        }
        else {
            yield result;
        }
    }
}
/**
 * Collects an iterable into an array. Having this as a callable function is useful for writing functional combinations.
 *
 * @param it - the iterable to collect
 * @returns an array with all the items in the iterable
 */
function collect(it) {
    return [...it];
}
/**
 * A helper function that allows categorizing items from an iterable into groups and running a different map function
 * for each group.
 *
 * @param source - the iterable to apply the selection and mapping to
 * @param select - a function that is applied to each item and produces a selector
 * @param delegates - a record of selectors to mapping functions
 * @returns a record of selectors to arrays of results produced by each delegate
 */
function selectMap(source, select, delegates) {
    const result = Object.fromEntries(Object.keys(delegates).map((k) => [k, []]));
    for (const value of source) {
        const k = select(value);
        result[k].push(delegates[k](value));
    }
    return result;
}
// #endregion

// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.
// Cache for scalar -> ProtoScalar map
const _protoScalarsMap = new WeakMap();
const _protoExternMap = new WeakMap();
/**
 * Create a worker function that converts the TypeSpec program to Protobuf and writes it to the file system.
 */
function createProtobufEmitter(program) {
    return async function doEmit(outDir, options) {
        // Convert the program to a set of proto files.
        const files = tspToProto(program, options);
        if (!program.compilerOptions.noEmit && !options?.noEmit && !program.hasError()) {
            for (const file of files) {
                // If the file has a package, emit it to a path that is shaped like the package name. Otherwise emit to
                // main.proto
                // Collisions have already been detected.
                const packageSlug = file.package?.split(".") ?? ["main"];
                const filePath = resolvePath(outDir, ...packageSlug.slice(0, -1));
                await program.host.mkdirp(filePath);
                await program.host.writeFile(resolvePath(filePath, packageSlug[packageSlug.length - 1] + ".proto"), writeProtoFile(file));
            }
        }
    };
}
/**
 * Create a set of proto files that represent the TypeSpec program.
 *
 * This is the meat of the emitter.
 */
function tspToProto(program, emitterOptions) {
    const packages = new Set(program.stateMap(state.package).keys());
    const serviceInterfaces = [...program.stateSet(state.service)];
    const declaredMessages = [...program.stateSet(state.message)];
    const declarationMap = new Map([...packages].map((p) => [p, []]));
    const visitedTypes = new Set();
    /**
     * Visits a model type, converting it into a message definition and adding it if it has not already been visited.
     * @param model - the model type to consider
     */
    function visitModel(model, source) {
        const modelPackage = getPackageOfType(program, model);
        const declarations = modelPackage && declarationMap.get(modelPackage);
        if (!declarations) {
            reportDiagnostic(program, {
                target: source,
                code: "model-not-in-package",
                format: { name: model.name },
            });
        }
        if (!visitedTypes.has(model)) {
            visitedTypes.add(model);
            declarations?.push(toMessage(model));
        }
    }
    /**
     * Visits an enum type, converting it into a Protobuf enum definition and adding it if it has not already been visited.
     */
    function visitEnum(e) {
        const modelPackage = getPackageOfType(program, e);
        const declarations = modelPackage && declarationMap.get(modelPackage);
        if (!visitedTypes.has(e)) {
            visitedTypes.add(e);
            const members = [...e.members.values()];
            // We only support enums where every variant is explicitly assigned an integer value
            if (members.some(({ value: v }) => v === undefined || typeof v !== "number" || !Number.isInteger(v))) {
                reportDiagnostic(program, {
                    target: e,
                    code: "unconvertible-enum",
                });
            }
            // we also only support enums where the first value is zero.
            if (members[0].value !== 0) {
                reportDiagnostic(program, {
                    target: members[0],
                    code: "unconvertible-enum",
                    messageId: "no-zero-first",
                });
            }
            declarations?.push(toEnum(e));
        }
    }
    const importMap = new Map([...packages].map((ns) => [ns, new Set()]));
    function typeWantsImport(program, t, path) {
        const packageNs = getPackageOfType(program, t);
        if (packageNs) {
            importMap.get(packageNs)?.add(path);
        }
    }
    const mapImportSourceInformation = new WeakMap();
    const effectiveModelCache = new Map();
    for (const packageNs of packages) {
        addDeclarationsOfPackage(packageNs);
    }
    // Emit a file per package.
    const files = [...packages].map((namespace) => {
        const details = program.stateMap(state.package).get(namespace);
        const packageOptionsRaw = details?.properties.get("options")?.type;
        const packageOptions = [...(packageOptionsRaw?.properties.entries() ?? [])]
            .map(([k, { type }]) => {
            // This condition is enforced by the definition of `dec package`
            if (type.kind === "Boolean" || type.kind === "String" || type.kind === "Number") {
                return [k, type.value];
            }
            else
                throw new Error(`Unexpected option type ${type.kind}`);
        })
            .filter((v) => !!v);
        return {
            package: details?.properties.get("name")?.type?.value,
            options: Object.fromEntries(packageOptions),
            imports: [...(importMap.get(namespace) ?? [])],
            declarations: declarationMap.get(namespace),
            source: namespace,
            doc: getDoc(program, namespace),
        };
    });
    checkForNamespaceCollisions(files);
    return files;
    /**
     * Recursively searches a namespace for declarations that should be reified as Protobuf.
     *
     * @param namespace - the namespace to analyze
     * @returns an array of declarations
     */
    function addDeclarationsOfPackage(namespace) {
        const eagerModels = new Set([
            ...declaredMessages.filter((m) => isDeclaredInNamespace(m, namespace)),
        ]);
        if (!emitterOptions["omit-unreachable-types"]) {
            // Add all models in the namespace that have `@field` on every property.
            for (const model of namespace.models.values()) {
                if ([...model.properties.values()].every((p) => program.stateMap(state.fieldIndex).has(p)) ||
                    program.stateSet(state.message).has(model)) {
                    eagerModels.add(model);
                }
            }
        }
        for (const model of eagerModels) {
            if (
            // Don't eagerly visit externs
            !program.stateMap(state.externRef).has(model) &&
                // Only eagerly visit models where every field has a field index annotation.
                ([...model.properties.values()].every((p) => program.stateMap(state.fieldIndex).has(p)) ||
                    // OR where the model has been explicitly marked as a message.
                    program.stateSet(state.message).has(model))) {
                visitModel(model, model);
            }
        }
        const interfacesInNamespace = new Set(serviceInterfaces.filter((iface) => isDeclaredInNamespace(iface, namespace)));
        // Each interface will be reified as a `service` declaration.
        const declarations = declarationMap.get(namespace);
        for (const iface of interfacesInNamespace) {
            declarations.push({
                kind: "service",
                name: iface.name,
                // The service's methods are just projections of the interface operations.
                operations: [...iface.operations.values()].map(toMethodFromOperation),
                doc: getDoc(program, iface),
            });
        }
    }
    // #region inline helpers
    /**
     * @param operation - the operation to convert
     * @returns a corresponding method declaration
     */
    function toMethodFromOperation(operation) {
        const streamingMode = program.stateMap(state.stream).get(operation) ?? 0 /* StreamingMode.None */;
        const isEmptyParams = operation.parameters.name === "" && operation.parameters.properties.size === 0;
        const input = isEmptyParams
            ? getCachedExternType(program, operation, "TypeSpec.Protobuf.WellKnown.Empty")
            : addImportSourceForProtoIfNeeded(program, addInputParams(operation.parameters, operation), operation, getEffectiveModelType(program, operation.parameters));
        return {
            kind: "method",
            stream: streamingMode,
            name: capitalize(operation.name),
            input,
            returns: addImportSourceForProtoIfNeeded(program, addReturnType(operation.returnType, operation), operation, operation.returnType),
            doc: getDoc(program, operation),
        };
    }
    /**
     * Checks a parameter Model satisfies the constraints for a Protobuf method input and adds it to the declarations,
     * returning a ProtoRef to the generated named message.
     *
     * @param model - the model to add
     * @returns a reference to the model's message
     */
    function addInputParams(paramsModel, operation) {
        const effectiveModel = computeEffectiveModel(paramsModel, capitalize(operation.name) + "Request");
        /* c8 ignore start */
        // Not sure if this can or can't actually happen at runtime, but we'll defensively handle it anyway.
        if (!effectiveModel) {
            reportDiagnostic(program, {
                code: "unsupported-input-type",
                messageId: "unconvertible",
                target: paramsModel,
            });
            return unreachable("unsupported input type");
        }
        /* c8 ignore stop */
        return checkExtern(effectiveModel, operation);
    }
    /**
     * Returns an extern ref if the given type is an instance of `Extern`, otherwise returns a ref to the model's name.
     */
    function checkExtern(model, relativeSource) {
        const extern = program.stateMap(state.externRef).get(model);
        if (extern) {
            typeWantsImport(program, relativeSource, extern[0]);
            return ref(extern[1]);
        }
        return ref(getModelName(model));
    }
    /**
     * Gets a cached intrinsic type. This will also attach desired imports to the relative reference source.
     */
    function getCachedExternType(program, relativeSource, name) {
        let cache = _protoExternMap.get(program);
        if (!cache) {
            cache = new Map();
            _protoExternMap.set(program, cache);
        }
        const cachedRef = cache.get(name);
        if (cachedRef) {
            const [source, ref] = cachedRef;
            typeWantsImport(program, relativeSource, source);
            return ref;
        }
        const [emptyType, diagnostics] = program.resolveTypeReference(name);
        if (!emptyType) {
            throw new Error(`Could not resolve the empty type: ${diagnostics.map((x) => formatDiagnostic(x)).join("\n")}`);
        }
        const extern = program.stateMap(state.externRef).get(emptyType);
        if (!extern) {
            throw new Error(`Unexpected: '${name}' was resolved but is not an extern type.`);
        }
        const [source, protoName] = extern;
        typeWantsImport(program, relativeSource, source);
        const result = ref(protoName);
        cache.set(name, [source, result]);
        return result;
    }
    /**
     * Checks that a return type is a Model and converts it to a message, adding it to the declarations and returning
     * a reference to its name.
     *
     * @param t - the model to add
     * @param operationName - the name of the originating operation, used to compute a synthetic model name if required
     * @returns a reference to the model's message
     */
    function addReturnType(t, operation) {
        switch (t.kind) {
            case "Model":
                return addReturnModel(t, operation);
            case "Intrinsic":
                return addIntrinsicType(t, operation);
            /* eslint-ignore-next-line no-fallthrough */
            default:
                reportDiagnostic(program, {
                    code: "unsupported-return-type",
                    target: getOperationReturnSyntaxTarget(operation),
                });
                return unreachable("unsupported return type");
        }
    }
    /**
     * Adds an intrinsic type. Intrinsics are assumed to map to Extern types, so this will add the appropriate import.
     *
     * @param t - the intrinsic type to add
     * @param relativeSource - the relative source of the type
     * @returns a reference to the type's message
     */
    function addIntrinsicType(t, relativeSource) {
        switch (t.name) {
            case "unknown":
                return getCachedExternType(program, relativeSource, "TypeSpec.Protobuf.WellKnown.Any");
            case "void": {
                return getCachedExternType(program, relativeSource, "TypeSpec.Protobuf.WellKnown.Empty");
            }
        }
        reportDiagnostic(program, {
            code: "unsupported-intrinsic",
            format: { name: t.name },
            target: t,
        });
        return unreachable("unsupported intrinsic type");
    }
    /**
     * Converts a TypeSpec Model to a Protobuf Ref in return position, adding a corresponding message if necessary.
     *
     * @param m - the model to add to the Protofile.
     * @returns a Protobuf reference to the model
     */
    function addReturnModel(m, operation) {
        const extern = program.stateMap(state.externRef).get(m);
        if (extern) {
            typeWantsImport(program, operation, extern[0]);
            return ref(extern[1]);
        }
        const effectiveModel = computeEffectiveModel(m, capitalize(operation.name) + "Response");
        if (effectiveModel) {
            return ref(getModelName(effectiveModel));
        }
        reportDiagnostic(program, {
            code: "unsupported-return-type",
            target: getOperationReturnSyntaxTarget(operation),
        });
        return unreachable("unsupported return type");
    }
    /**
     * Converts a TypeSpec type to a Protobuf type, adding a corresponding message if necessary.
     *
     * @param t - the type to add to the ProtoFile.
     * @returns a Protobuf type corresponding to the given type
     */
    function addType(t, relativeSource) {
        // Exit early if this type is an extern.
        const extern = program.stateMap(state.externRef).get(t);
        if (extern) {
            typeWantsImport(program, relativeSource, extern[0]);
            return ref(extern[1]);
        }
        if (isMap(program, t)) {
            const mapType = mapToProto(t, relativeSource);
            mapImportSourceInformation.set(mapType, [relativeSource, t]);
            return mapType;
        }
        // Arrays transform into repeated fields, so we'll silently replace `t` with the array's member if this is an array.
        // The `repeated` keyword will be added when the field is composed.
        if (isArray(t)) {
            return arrayToProto(t, relativeSource);
        }
        switch (t.kind) {
            case "Model":
                // If we came from another model and this model is anonymous, then we can't reference it by name.
                if (t.name === "" && relativeSource.kind === "Model") {
                    reportDiagnostic(program, {
                        code: "anonymous-model",
                        target: t,
                    });
                    return unreachable("anonymous model");
                }
                visitModel(t, relativeSource);
                return ref(getModelName(t));
            case "Enum":
                visitEnum(t);
                return ref(t.name);
            case "Scalar":
                return scalarToProto(t);
            case "Intrinsic":
                return addIntrinsicType(t, relativeSource);
            default:
                reportDiagnostic(program, {
                    code: "unsupported-field-type",
                    messageId: "unconvertible",
                    format: {
                        type: t.kind,
                    },
                    target: t,
                });
                return unreachable("unsupported field type");
        }
    }
    function mapToProto(t, relativeSource) {
        const [keyType, valueType] = t.templateMapper.args;
        compilerAssert(isType(keyType), "Cannot be a value type");
        compilerAssert(isType(valueType), "Cannot be a value type");
        // A map's value cannot be another map.
        if (isMap(program, keyType)) {
            reportDiagnostic(program, {
                code: "unsupported-field-type",
                messageId: "recursive-map",
                target: valueType,
            });
            return unreachable("recursive map");
        }
        // This is a core compile error.
        if (!keyType || !valueType)
            return unreachable("nonexistent map key or value type");
        // Key constraint (integral | string) is enforced by the type constraint on the `Map<>` type.
        const keyProto = addType(keyType, relativeSource);
        const valueProto = addType(valueType, relativeSource);
        return map(keyProto[1], valueType.kind === "Model"
            ? addImportSourceForProtoIfNeeded(program, valueProto, relativeSource, valueType)
            : valueProto);
    }
    function arrayToProto(t, relativeSource) {
        const valueType = t.templateMapper.args[0];
        compilerAssert(isType(valueType), "Cannot be a value type");
        // Nested arrays are not supported.
        if (isArray(valueType)) {
            reportDiagnostic(program, {
                code: "nested-array",
                target: t,
            });
            return ref("<unreachable>");
        }
        return addType(valueType, relativeSource);
    }
    function getProtoScalarsMap(program) {
        // The type references are different object identities in different programs, so we need to cache the map per program.
        // This really only affects tests in our current use case, but someone could be using the compiler API to compile
        // multiple programs and it also affects that.
        let scalarMap;
        if (_protoScalarsMap.has(program)) {
            scalarMap = _protoScalarsMap.get(program);
        }
        else {
            const entries = [
                [program.resolveTypeReference("TypeSpec.bytes"), scalar("bytes")],
                [program.resolveTypeReference("TypeSpec.boolean"), scalar("bool")],
                [program.resolveTypeReference("TypeSpec.string"), scalar("string")],
                [program.resolveTypeReference("TypeSpec.int32"), scalar("int32")],
                [program.resolveTypeReference("TypeSpec.int64"), scalar("int64")],
                [program.resolveTypeReference("TypeSpec.uint32"), scalar("uint32")],
                [program.resolveTypeReference("TypeSpec.uint64"), scalar("uint64")],
                [program.resolveTypeReference("TypeSpec.float32"), scalar("float")],
                [program.resolveTypeReference("TypeSpec.float64"), scalar("double")],
                [program.resolveTypeReference("TypeSpec.Protobuf.sfixed32"), scalar("sfixed32")],
                [program.resolveTypeReference("TypeSpec.Protobuf.sfixed64"), scalar("sfixed64")],
                [program.resolveTypeReference("TypeSpec.Protobuf.sint32"), scalar("sint32")],
                [program.resolveTypeReference("TypeSpec.Protobuf.sint64"), scalar("sint64")],
                [program.resolveTypeReference("TypeSpec.Protobuf.fixed32"), scalar("fixed32")],
                [program.resolveTypeReference("TypeSpec.Protobuf.fixed64"), scalar("fixed64")],
            ];
            for (const [[type, diagnostics]] of entries) {
                if (!type) {
                    const diagnosticString = diagnostics.map((x) => formatDiagnostic(x)).join("\n");
                    throw new Error(`Failed to construct TypeSpec -> Protobuf scalar map. Unexpected failure to resolve TypeSpec scalar: ${diagnosticString}`);
                }
            }
            scalarMap = new Map(entries.map(([[type], scalar]) => [type, scalar]));
            _protoScalarsMap.set(program, scalarMap);
        }
        // Lazy initialize this map of known proto scalars.
        return scalarMap;
    }
    function scalarToProto(t) {
        const fullName = getTypeName(t);
        const protoType = getProtoScalarsMap(program).get(t);
        if (!protoType) {
            if (t.baseScalar) {
                return scalarToProto(t.baseScalar);
            }
            else {
                reportDiagnostic(program, {
                    code: "unsupported-field-type",
                    messageId: "unknown-scalar",
                    format: {
                        name: fullName,
                    },
                    target: t,
                });
                return unreachable("unknown scalar");
            }
        }
        return protoType;
    }
    function computeEffectiveModel(model, anonymousModelName) {
        if (effectiveModelCache.has(model))
            return effectiveModelCache.get(model);
        let effectiveModel = getEffectiveModelType(program, model);
        if (effectiveModel.name === "") {
            // Name the model automatically if it is anonymous
            effectiveModel = program.checker.createAndFinishType({
                ...model,
                name: anonymousModelName,
            });
        }
        if (!program.stateMap(state.externRef).has(effectiveModel)) {
            visitModel(effectiveModel, model);
        }
        effectiveModelCache.set(model, effectiveModel);
        return effectiveModel;
    }
    // #endregion
    function checkForNamespaceCollisions(files) {
        const namespaces = new Set();
        for (const file of files) {
            if (namespaces.has(file.package)) {
                reportDiagnostic(program, {
                    code: "namespace-collision",
                    format: {
                        name: file.package ? `"${file.package}"` : "<empty>",
                    },
                    target: file.source,
                });
            }
            namespaces.add(file.package);
        }
    }
    /**
     * @param model - the Model to convert
     * @returns a corresponding message declaration
     */
    function toMessage(model) {
        return {
            kind: "message",
            name: getModelName(model),
            reservations: program.stateMap(state.reserve).get(model),
            declarations: [...model.properties.values()].map((f) => toMessageBodyDeclaration(f, model)),
            doc: getDoc(program, model),
        };
    }
    function getModelName(model) {
        const friendlyName = getFriendlyName(program, model);
        if (friendlyName)
            return capitalize(friendlyName);
        const templateArguments = isTemplateInstance(model) ? model.templateMapper.args : [];
        const prefix = templateArguments
            .map(function getTypePrefixName(arg, idx) {
            if ("name" in arg && typeof arg.name === "string" && arg.name !== "")
                return capitalize(arg.name);
            else {
                reportDiagnostic.once(program, {
                    code: "unspeakable-template-argument",
                    // TODO-WILL - I'd rather attach the diagnostic to the template argument, but it's the best I can do for
                    // now to attach it to the model itself.
                    target: model,
                    format: {
                        name: model.name,
                    },
                });
                return `T${idx}`;
            }
        })
            .join("");
        return prefix + capitalize(model.name);
    }
    /**
     * @param property - the ModelProperty to convert
     * @returns a corresponding declaration
     */
    function toMessageBodyDeclaration(property, model) {
        if (property.type.kind === "Union") {
            // Unions are difficult to represent in protobuf, so for now we don't support them.
            // See : https://github.com/microsoft/typespec/issues/1854
            reportDiagnostic(program, {
                code: "unsupported-field-type",
                messageId: "union",
                target: property,
            });
            return unreachable("union");
        }
        const fieldIndex = program.stateMap(state.fieldIndex).get(property);
        const fieldIndexNode = property.decorators.find((d) => d.decorator === $field)?.args[0].node;
        if (fieldIndex === undefined) {
            reportDiagnostic(program, {
                code: "field-index",
                messageId: "missing",
                format: {
                    name: property.name,
                },
                target: property,
            });
        }
        if (fieldIndex && !fieldIndexNode)
            throw new Error("Failed to recover field decorator argument.");
        const reservations = program.stateMap(state.reserve).get(model);
        if (reservations) {
            for (const reservation of reservations) {
                if (typeof reservation === "string" && reservation === property.name) {
                    reportDiagnostic(program, {
                        code: "field-name",
                        messageId: "user-reserved",
                        format: {
                            name: property.name,
                        },
                        target: getPropertyNameSyntaxTarget(property),
                    });
                }
                else if (fieldIndex !== undefined &&
                    typeof reservation === "number" &&
                    reservation === fieldIndex) {
                    reportDiagnostic(program, {
                        code: "field-index",
                        messageId: "user-reserved",
                        format: {
                            index: fieldIndex.toString(),
                        },
                        // Fail over to using the model if the field index node is missing... this should never occur but it's the
                        // simplest way to satisfy the type system.
                        target: fieldIndexNode ?? model,
                    });
                }
                else if (fieldIndex !== undefined &&
                    Array.isArray(reservation) &&
                    fieldIndex >= reservation[0] &&
                    fieldIndex <= reservation[1]) {
                    reportDiagnostic(program, {
                        code: "field-index",
                        messageId: "user-reserved-range",
                        format: {
                            index: fieldIndex.toString(),
                        },
                        target: fieldIndexNode ?? model,
                    });
                }
            }
        }
        const field = {
            kind: "field",
            name: property.name,
            type: addImportSourceForProtoIfNeeded(program, addType(property.type, model), model, property.type),
            index: program.stateMap(state.fieldIndex).get(property),
            doc: getDoc(program, property),
        };
        // Determine if the property type is an array
        if (isArray(property.type))
            field.repeated = true;
        return field;
    }
    /**
     * @param e - the Enum to convert
     * @returns a corresponding protobuf enum declaration
     *
     * INVARIANT: the enum's members must be integer values
     */
    function toEnum(e) {
        const needsAlias = new Set([...e.members.values()].map((v) => v.value)).size !== e.members.size;
        return {
            kind: "enum",
            name: e.name,
            allowAlias: needsAlias,
            variants: [...e.members.values()].map((variant) => ({
                kind: "variant",
                name: variant.name,
                value: variant.value,
                doc: getDoc(program, variant),
            })),
            doc: getDoc(program, e),
        };
    }
    function getPackageOfType(program, t) {
        /* c8 ignore start */
        // Most of this should be unreachable, but we'll guard it with diagnostics anyway in case of eventual synthetic types.
        switch (t.kind) {
            case "Intrinsic":
                // Intrinsics are all handled explicitly.
                return null;
            case "Enum":
            case "Model":
            case "Union":
            case "Interface":
                if (!t.namespace) {
                    return null;
                }
                else {
                    return getPackageOfType(program, t.namespace);
                }
            case "Operation": {
                const logicalParent = t.interface ?? t.namespace;
                if (!logicalParent) {
                    return null;
                }
                else {
                    return getPackageOfType(program, logicalParent);
                }
            }
            case "Namespace":
                if (packages.has(t))
                    return t;
                if (!t.namespace) {
                    return null;
                }
                else {
                    return getPackageOfType(program, t.namespace);
                }
        }
        /* c8 ignore stop */
    }
    function addImportSourceForProtoIfNeeded(program, pt, dependent, dependency) {
        {
            // Early escape for intrinsics
            if (dependency.kind === "Intrinsic") {
                // Intrinsics and imports are handled explicitly by the emitter.
                return pt;
            }
        }
        {
            // Early escape for externs
            let effectiveModel;
            if (program.stateMap(state.externRef).has(dependency) ||
                (dependency.kind === "Model" &&
                    (effectiveModel = effectiveModelCache.get(dependency)) &&
                    program.stateMap(state.externRef).has(effectiveModel))) {
                return pt;
            }
        }
        if (isArray(dependency)) {
            return addImportSourceForProtoIfNeeded(program, pt, dependent, dependency.templateMapper.args[0]);
        }
        try {
            // If we had an error producing an "unreachable" type, we would actually reach it during validation below, so the
            // try/catch allows us to pass the unreachable back up the chain.
            return matchType(pt, {
                map(k, v) {
                    const mapInfo = mapImportSourceInformation.get(pt);
                    return mapInfo !== undefined
                        ? map(k, addImportSourceForProtoIfNeeded(program, v, mapInfo[0], mapInfo[1]))
                        : pt;
                },
                scalar() {
                    return pt;
                },
                ref(r) {
                    const [dependentPackage, dependencyPackage] = [
                        getPackageOfType(program, dependent),
                        getPackageOfType(program, dependency),
                    ];
                    if (dependentPackage === null ||
                        dependencyPackage === null ||
                        dependentPackage === dependencyPackage)
                        return pt;
                    const dependencyDetails = program.stateMap(state.package).get(dependencyPackage);
                    const dependencyPackageName = dependencyDetails?.properties.get("name")?.type?.value;
                    const dependencyPackagePrefix = dependencyPackageName === undefined || dependencyPackageName === ""
                        ? ""
                        : dependencyPackageName + ".";
                    const dependencyFileName = (dependencyPackageName?.split(".") ?? ["main"]).join("/") + ".proto";
                    importMap.get(dependentPackage)?.add(dependencyFileName);
                    return ref(dependencyPackagePrefix + r);
                },
            });
        }
        catch {
            return pt;
        }
    }
}
function isArray(t) {
    return t.kind === "Model" && t.name === "Array" && t.namespace?.name === "TypeSpec";
}
/**
 * Simple utility function to capitalize a string.
 */
function capitalize(s) {
    return (s.slice(0, 1).toUpperCase() + s.slice(1));
}
/**
 * Gets the syntactic return type target for an operation.
 *
 * Helps us squiggle the right things for operation return types.
 *
 * See https://github.com/microsoft/typespec/issues/1650. This issue tracks helpers for doing this without requiring
 * emitters to implement this functionality.
 */
function getOperationReturnSyntaxTarget(op) {
    const signature = op.node.signature;
    switch (signature.kind) {
        case SyntaxKind.OperationSignatureDeclaration:
            return signature.returnType;
        case SyntaxKind.OperationSignatureReference:
            return op;
        default:
            throw new Error(`Internal Emitter Error: reached unreachable operation signature: ${op.node.signature.kind}`);
    }
}
/**
 * Gets the syntactic position of a model property name.
 *
 * See https://github.com/microsoft/typespec/issues/1650. This issue tracks helpers for doing this without requiring
 * emitters to implement this functionality.
 */
function getPropertyNameSyntaxTarget(property) {
    const node = property.node;
    switch (node.kind) {
        case SyntaxKind.ModelProperty:
        case SyntaxKind.ObjectLiteralProperty:
            return node.id;
        case SyntaxKind.ModelSpreadProperty:
            return node;
        case SyntaxKind.ProjectionModelProperty:
        case SyntaxKind.ProjectionModelSpreadProperty:
            return property;
        default:
            throw new Error(`Internal Emitter Error: reached unreachable model property node: ${property.node.kind}`);
    }
}

// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.
/**
 * # @typespec/protobuf : Protobuf/gRPC Emitter and Decorators for TypeSpec
 *
 * This module defines an emitter and decorator library for TypeSpec that enables specifying Protobuf services and models.
 */
/**
 * The maximum field index allowed by Protocol Buffers.
 */
const MAX_FIELD_INDEX = 2 ** 29 - 1;
/**
 * The field range between 19000 and 19999 is reserved for Protobuf client implementations.
 */
const IMPLEMENTATION_RESERVED_RANGE = [19000, 19999];
/**
 * Defined in the [ProtoBuf Language Spec](https://developers.google.com/protocol-buffers/docs/reference/proto3-spec#identifiers).
 *
 * ident = letter \{ letter | decimalDigit | "_" \}
 * fullIdent = ident \{ "." ident \}
 */
const PROTO_FULL_IDENT = /([a-zA-Z][a-zA-Z0-9_]*)+/;
/**
 * Decorate an interface as a service, indicating that it represents a Protobuf `service` declaration.
 *
 * @param ctx - decorator context
 * @param target - the decorated interface
 */
function $service(ctx, target) {
    ctx.program.stateSet(state.service).add(target);
}
/**
 * Declare a Protobuf package.
 *
 * @param ctx - decorator context
 * @param target - target decorator namespace
 */
const $package = (ctx, target, details) => {
    ctx.program.stateMap(state.package).set(target, details);
};
/**
 * Determines whether a type represents a Protobuf map.
 *
 * @param program - the program context
 * @param m - the type to test
 * @returns true if the internal representation of a Protobuf map is bound to this type.
 */
function isMap(program, m) {
    return program.stateSet(state._map).has(m);
}
/**
 * Binds the internal representation of a Protobuf map.
 * @internal
 * @param ctx
 * @param target
 */
function $_map(ctx, target) {
    ctx.program.stateSet(state._map).add(target);
}
const $externRef = (ctx, target, path, name) => {
    ctx.program
        .stateMap(state.externRef)
        .set(target, [path.value, name.value]);
};
const $stream = (ctx, target, mode) => {
    const emitStreamingMode = {
        Duplex: 3 /* StreamingMode.Duplex */,
        In: 2 /* StreamingMode.In */,
        Out: 1 /* StreamingMode.Out */,
        None: 0 /* StreamingMode.None */,
    }[mode.name];
    ctx.program.stateMap(state.stream).set(target, emitStreamingMode);
};
const $reserve = (ctx, target, ...reservations) => {
    const finalReservations = reservations.filter((v) => v != null);
    ctx.program.stateMap(state.reserve).set(target, finalReservations);
};
const $message = (ctx, target) => {
    ctx.program.stateSet(state.message).add(target);
};
/**
 * Decorate a model property with a field index. Field indices are required for all fields of emitted messages.
 *
 * @param param0
 * @param target
 * @param fieldIndex
 * @returns
 */
const $field = (ctx, target, fieldIndex) => {
    if (!Number.isInteger(fieldIndex) || fieldIndex <= 0) {
        reportDiagnostic(ctx.program, {
            code: "field-index",
            messageId: "invalid",
            format: {
                index: String(fieldIndex),
            },
            target,
        });
        return;
    }
    else if (fieldIndex > MAX_FIELD_INDEX) {
        reportDiagnostic(ctx.program, {
            code: "field-index",
            messageId: "out-of-bounds",
            format: {
                index: String(fieldIndex),
                max: String(MAX_FIELD_INDEX + 1),
            },
            target,
        });
        return;
    }
    else if (fieldIndex >= IMPLEMENTATION_RESERVED_RANGE[0] &&
        fieldIndex <= IMPLEMENTATION_RESERVED_RANGE[1]) {
        reportDiagnostic(ctx.program, {
            code: "field-index",
            messageId: "reserved",
            format: {
                index: String(fieldIndex),
            },
            target,
        });
    }
    ctx.program.stateMap(state.fieldIndex).set(target, fieldIndex);
};
/**
 * Emitter main function.
 *
 * @param program - the program to emit
 */
async function $onEmit(ctx) {
    const emitter = createProtobufEmitter(ctx.program);
    await emitter(resolvePath(ctx.emitterOutputDir), ctx.options);
}
/**
 * Validation function
 */
async function $onValidate(program) {
    // Is this correct? See https://github.com/microsoft/typespec/issues/1859
    /* c8 ignore next 6 */
    if (program.compilerOptions.noEmit) {
        const options = program.emitters.find((e) => e.emitFunction === $onEmit)
            ?.options;
        const emitter = createProtobufEmitter(program);
        await emitter("", options);
    }
}

/** @internal */
const $decorators = {
    "TypeSpec.Protobuf": {
        message: $message,
        field: $field,
        reserve: $reserve,
        service: $service,
        package: $package,
        stream: $stream,
    },
    "TypeSpec.Protobuf.Private": {
        externRef: $externRef,
        _map: $_map,
    },
};

var f1 = /*#__PURE__*/Object.freeze({
    __proto__: null,
    $decorators: $decorators,
    $lib: TypeSpecProtobufLibrary
});

const namespace = "TypeSpec.Protobuf";
const $lib = TypeSpecProtobufLibrary;

var f0 = /*#__PURE__*/Object.freeze({
    __proto__: null,
    $_map: $_map,
    $decorators: $decorators,
    $externRef: $externRef,
    $field: $field,
    $lib: $lib,
    $message: $message,
    $onEmit: $onEmit,
    $onValidate: $onValidate,
    $package: $package,
    $reserve: $reserve,
    $service: $service,
    $stream: $stream,
    PROTO_FULL_IDENT: PROTO_FULL_IDENT,
    isMap: isMap,
    namespace: namespace
});

const TypeSpecJSSources = {
"dist/src/index.js": f0,
"dist/src/tsp-index.js": f1,
};
const TypeSpecSources = {
  "package.json": "{\"name\":\"@typespec/protobuf\",\"version\":\"0.64.0\",\"author\":\"Microsoft Corporation\",\"description\":\"TypeSpec library and emitter for Protobuf (gRPC)\",\"homepage\":\"https://github.com/microsoft/typespec\",\"readme\":\"https://github.com/microsoft/typespec/blob/main/packages/protobuf/README.md\",\"license\":\"MIT\",\"repository\":{\"type\":\"git\",\"url\":\"git+https://github.com/microsoft/typespec.git\"},\"bugs\":{\"url\":\"https://github.com/microsoft/typespec/issues\"},\"keywords\":[\"typespec\",\"protobuf\",\"grpc\"],\"main\":\"dist/src/index.js\",\"exports\":{\".\":{\"typespec\":\"./lib/proto.tsp\",\"types\":\"./dist/src/index.d.ts\",\"default\":\"./dist/src/index.js\"},\"./testing\":\"./dist/src/testing/index.js\"},\"type\":\"module\",\"tspMain\":\"lib/proto.tsp\",\"scripts\":{\"clean\":\"rimraf ./dist ./temp\",\"build\":\"npm run gen-extern-signature && tsc -p .\",\"watch\":\"tsc -p . --watch\",\"gen-extern-signature\":\"tspd --enable-experimental gen-extern-signature .\",\"test\":\"vitest run\",\"test:ci\":\"vitest run --coverage --reporter=junit --reporter=default\",\"lint\":\"eslint . --max-warnings=0\",\"lint:fix\":\"eslint . --fix\",\"regen-docs\":\"tspd doc .  --enable-experimental  --output-dir ../../website/src/content/docs/docs/emitters/protobuf/reference\"},\"peerDependencies\":{\"@typespec/compiler\":\"workspace:~\"},\"devDependencies\":{\"@types/micromatch\":\"^4.0.9\",\"@types/node\":\"~22.7.9\",\"@typespec/compiler\":\"workspace:~\",\"@typespec/tspd\":\"workspace:~\",\"@vitest/coverage-v8\":\"^2.1.5\",\"@vitest/ui\":\"^2.1.2\",\"c8\":\"^10.1.2\",\"micromatch\":\"^4.0.8\",\"rimraf\":\"~6.0.1\",\"typescript\":\"~5.6.3\",\"vitest\":\"^2.1.5\"}}",
  "../compiler/lib/intrinsics.tsp": "import \"../dist/src/lib/intrinsic/tsp-index.js\";\nimport \"./prototypes.tsp\";\n\n// This file contains all the intrinsic types of typespec. Everything here will always be loaded\nnamespace TypeSpec;\n\n/**\n * Represent a byte array\n */\nscalar bytes;\n\n/**\n * A numeric type\n */\nscalar numeric;\n\n/**\n * A whole number. This represent any `integer` value possible.\n * It is commonly represented as `BigInteger` in some languages.\n */\nscalar integer extends numeric;\n\n/**\n * A number with decimal value\n */\nscalar float extends numeric;\n\n/**\n * A 64-bit integer. (`-9,223,372,036,854,775,808` to `9,223,372,036,854,775,807`)\n */\nscalar int64 extends integer;\n\n/**\n * A 32-bit integer. (`-2,147,483,648` to `2,147,483,647`)\n */\nscalar int32 extends int64;\n\n/**\n * A 16-bit integer. (`-32,768` to `32,767`)\n */\nscalar int16 extends int32;\n\n/**\n * A 8-bit integer. (`-128` to `127`)\n */\nscalar int8 extends int16;\n\n/**\n * A 64-bit unsigned integer (`0` to `18,446,744,073,709,551,615`)\n */\nscalar uint64 extends integer;\n\n/**\n * A 32-bit unsigned integer (`0` to `4,294,967,295`)\n */\nscalar uint32 extends uint64;\n\n/**\n * A 16-bit unsigned integer (`0` to `65,535`)\n */\nscalar uint16 extends uint32;\n\n/**\n * A 8-bit unsigned integer (`0` to `255`)\n */\nscalar uint8 extends uint16;\n\n/**\n * An integer that can be serialized to JSON (`−9007199254740991 (−(2^53 − 1))` to `9007199254740991 (2^53 − 1)` )\n */\nscalar safeint extends int64;\n\n/**\n * A 64 bit floating point number. (`±5.0 × 10^−324` to `±1.7 × 10^308`)\n */\nscalar float64 extends float;\n\n/**\n * A 32 bit floating point number. (`±1.5 x 10^−45` to `±3.4 x 10^38`)\n */\nscalar float32 extends float64;\n\n/**\n * A decimal number with any length and precision. This represent any `decimal` value possible.\n * It is commonly represented as `BigDecimal` in some languages.\n */\nscalar decimal extends numeric;\n\n/**\n * A 128-bit decimal number.\n */\nscalar decimal128 extends decimal;\n\n/**\n * A sequence of textual characters.\n */\nscalar string;\n\n/**\n * A date on a calendar without a time zone, e.g. \"April 10th\"\n */\nscalar plainDate {\n  /**\n   * Create a plain date from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = plainTime.fromISO(\"2024-05-06\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * A time on a clock without a time zone, e.g. \"3:00 am\"\n */\nscalar plainTime {\n  /**\n   * Create a plain time from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = plainTime.fromISO(\"12:34\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * An instant in coordinated universal time (UTC)\"\n */\nscalar utcDateTime {\n  /**\n   * Create a date from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = utcDateTime.fromISO(\"2024-05-06T12:20-12Z\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * A date and time in a particular time zone, e.g. \"April 10th at 3:00am in PST\"\n */\nscalar offsetDateTime {\n  /**\n   * Create a date from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = offsetDateTime.fromISO(\"2024-05-06T12:20-12-0700\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * A duration/time period. e.g 5s, 10h\n */\nscalar duration {\n  /**\n   * Create a duration from an ISO 8601 string.\n   * @example\n   *\n   * ```tsp\n   * const time = duration.fromISO(\"P1Y1D\");\n   * ```\n   */\n  init fromISO(value: string);\n}\n\n/**\n * Boolean with `true` and `false` values.\n */\nscalar boolean;\n\n/**\n * @dev Array model type, equivalent to `Element[]`\n * @template Element The type of the array elements\n */\n@indexer(integer, Element)\nmodel Array<Element> {}\n\n/**\n * @dev Model with string properties where all the properties have type `Property`\n * @template Element The type of the properties\n */\n@indexer(string, Element)\nmodel Record<Element> {}\n",
  "../compiler/lib/prototypes.tsp": "namespace TypeSpec.Prototypes;\n\nextern dec getter(target: unknown);\n\nnamespace Types {\n  interface ModelProperty {\n    @getter type(): unknown;\n  }\n\n  interface Operation {\n    @getter returnType(): unknown;\n    @getter parameters(): unknown;\n  }\n\n  interface Array<TElementType> {\n    @getter elementType(): TElementType;\n  }\n}\n",
  "../compiler/lib/std/main.tsp": "// TypeSpec standard library. Everything in here can be omitted by using `--nostdlib` cli flag or `nostdlib` in the config.\nimport \"./types.tsp\";\nimport \"./decorators.tsp\";\nimport \"./reflection.tsp\";\nimport \"./projected-names.tsp\";\nimport \"./visibility.tsp\";\n",
  "../compiler/lib/std/types.tsp": "namespace TypeSpec;\n\n/**\n * Represent a 32-bit unix timestamp datetime with 1s of granularity.\n * It measures time by the number of seconds that have elapsed since 00:00:00 UTC on 1 January 1970.\n */\n@encode(\"unixTimestamp\", int32)\nscalar unixTimestamp32 extends utcDateTime;\n\n/**\n * Represent a model\n */\n// Deprecated June 2023 sprint\n#deprecated \"object is deprecated. Please use {} for an empty model, `Record<unknown>` for a record with unknown property types, `unknown[]` for an array.\"\nmodel object {}\n\n/**\n * Represent a URL string as described by https://url.spec.whatwg.org/\n */\nscalar url extends string;\n\n/**\n * Represents a collection of optional properties.\n *\n * @template Source An object whose spread properties are all optional.\n */\n@doc(\"The template for adding optional properties.\")\n@withOptionalProperties\nmodel OptionalProperties<Source> {\n  ...Source;\n}\n\n/**\n * Represents a collection of updateable properties.\n *\n * @template Source An object whose spread properties are all updateable.\n */\n@doc(\"The template for adding updateable properties.\")\n@withUpdateableProperties\nmodel UpdateableProperties<Source> {\n  ...Source;\n}\n\n/**\n * Represents a collection of omitted properties.\n *\n * @template Source An object whose properties are spread.\n * @template Keys The property keys to omit.\n */\n@doc(\"The template for omitting properties.\")\n@withoutOmittedProperties(Keys)\nmodel OmitProperties<Source, Keys extends string> {\n  ...Source;\n}\n\n/**\n * Represents a collection of properties with only the specified keys included.\n *\n * @template Source An object whose properties are spread.\n * @template Keys The property keys to include.\n */\n@doc(\"The template for picking properties.\")\n@withPickedProperties(Keys)\nmodel PickProperties<Source, Keys extends string> {\n  ...Source;\n}\n\n/**\n * Represents a collection of properties with default values omitted.\n *\n * @template Source An object whose spread property defaults are all omitted.\n */\n@withoutDefaultValues\nmodel OmitDefaults<Source> {\n  ...Source;\n}\n\n/**\n * Applies a visibility setting to a collection of properties.\n *\n * @template Source An object whose properties are spread.\n * @template Visibility The visibility to apply to all properties.\n */\n@doc(\"The template for setting the default visibility of key properties.\")\n@withDefaultKeyVisibility(Visibility)\nmodel DefaultKeyVisibility<Source, Visibility extends valueof string> {\n  ...Source;\n}\n",
  "../compiler/lib/std/decorators.tsp": "import \"../../dist/src/lib/tsp-index.js\";\n\nusing TypeSpec.Reflection;\n\nnamespace TypeSpec;\n\n/**\n * Typically a short, single-line description.\n * @param summary Summary string.\n *\n * @example\n * ```typespec\n * @summary(\"This is a pet\")\n * model Pet {}\n * ```\n */\nextern dec summary(target: unknown, summary: valueof string);\n\n/**\n * Attach a documentation string.\n * @param doc Documentation string\n * @param formatArgs Record with key value pair that can be interpolated in the doc.\n *\n * @example\n * ```typespec\n * @doc(\"Represent a Pet available in the PetStore\")\n * model Pet {}\n * ```\n */\nextern dec doc(target: unknown, doc: valueof string, formatArgs?: {});\n\n/**\n * Attach a documentation string to describe the successful return types of an operation.\n * If an operation returns a union of success and errors it only describes the success. See `@errorsDoc` for error documentation.\n * @param doc Documentation string\n *\n * @example\n * ```typespec\n * @returnsDoc(\"Returns doc\")\n * op get(): Pet | NotFound;\n * ```\n */\nextern dec returnsDoc(target: Operation, doc: valueof string);\n\n/**\n * Attach a documentation string to describe the error return types of an operation.\n * If an operation returns a union of success and errors it only describes the errors. See `@returnsDoc` for success documentation.\n * @param doc Documentation string\n *\n * @example\n * ```typespec\n * @errorsDoc(\"Errors doc\")\n * op get(): Pet | NotFound;\n * ```\n */\nextern dec errorsDoc(target: Operation, doc: valueof string);\n\n/**\n * Mark this type as deprecated.\n *\n * NOTE: This decorator **should not** be used, use the `#deprecated` directive instead.\n *\n * @deprecated Use the `#deprecated` [directive](https://typespec.io/docs/language-basics/directives/#deprecated) instead.\n * @param message Deprecation message.\n *\n * @example\n *\n * Use the `#deprecated` directive instead:\n *\n * ```typespec\n * #deprecated \"Use ActionV2\"\n * op Action<Result>(): Result;\n * ```\n */\n#deprecated \"@deprecated decorator is deprecated. Use the `#deprecated` directive instead.\"\nextern dec deprecated(target: unknown, message: valueof string);\n\n/**\n * Service options.\n */\nmodel ServiceOptions {\n  /**\n   * Title of the service.\n   */\n  title?: string;\n\n  /**\n   * Version of the service.\n   */\n  version?: string;\n}\n\n/**\n * Mark this namespace as describing a service and configure service properties.\n * @param options Optional configuration for the service.\n *\n * @example\n * ```typespec\n * @service\n * namespace PetStore;\n * ```\n *\n * @example Setting service title\n * ```typespec\n * @service({title: \"Pet store\"})\n * namespace PetStore;\n * ```\n *\n * @example Setting service version\n * ```typespec\n * @service({version: \"1.0\"})\n * namespace PetStore;\n * ```\n */\nextern dec service(target: Namespace, options?: ServiceOptions);\n\n/**\n * Specify that this model is an error type. Operations return error types when the operation has failed.\n *\n * @example\n * ```typespec\n * @error\n * model PetStoreError {\n *   code: string;\n *   message: string;\n * }\n * ```\n */\nextern dec error(target: Model);\n\n/**\n * Specify a known data format hint for this string type. For example `uuid`, `uri`, etc.\n * This differs from the `@pattern` decorator which is meant to specify a regular expression while `@format` accepts a known format name.\n * The format names are open ended and are left to emitter to interpret.\n *\n * @param format format name.\n *\n * @example\n * ```typespec\n * @format(\"uuid\")\n * scalar uuid extends string;\n * ```\n */\nextern dec format(target: string | bytes | ModelProperty, format: valueof string);\n\n/**\n * Specify the the pattern this string should respect using simple regular expression syntax.\n * The following syntax is allowed: alternations (`|`), quantifiers (`?`, `*`, `+`, and `{ }`), wildcard (`.`), and grouping parentheses.\n * Advanced features like look-around, capture groups, and references are not supported.\n *\n * This decorator may optionally provide a custom validation _message_. Emitters may choose to use the message to provide\n * context when pattern validation fails. For the sake of consistency, the message should be a phrase that describes in\n * plain language what sort of content the pattern attempts to validate. For example, a complex regular expression that\n * validates a GUID string might have a message like \"Must be a valid GUID.\"\n *\n * @param pattern Regular expression.\n * @param validationMessage Optional validation message that may provide context when validation fails.\n *\n * @example\n * ```typespec\n * @pattern(\"[a-z]+\", \"Must be a string consisting of only lower case letters and of at least one character.\")\n * scalar LowerAlpha extends string;\n * ```\n */\nextern dec pattern(\n  target: string | bytes | ModelProperty,\n  pattern: valueof string,\n  validationMessage?: valueof string\n);\n\n/**\n * Specify the minimum length this string type should be.\n * @param value Minimum length\n *\n * @example\n * ```typespec\n * @minLength(2)\n * scalar Username extends string;\n * ```\n */\nextern dec minLength(target: string | ModelProperty, value: valueof integer);\n\n/**\n * Specify the maximum length this string type should be.\n * @param value Maximum length\n *\n * @example\n * ```typespec\n * @maxLength(20)\n * scalar Username extends string;\n * ```\n */\nextern dec maxLength(target: string | ModelProperty, value: valueof integer);\n\n/**\n * Specify the minimum number of items this array should have.\n * @param value Minimum number\n *\n * @example\n * ```typespec\n * @minItems(1)\n * model Endpoints is string[];\n * ```\n */\nextern dec minItems(target: unknown[] | ModelProperty, value: valueof integer);\n\n/**\n * Specify the maximum number of items this array should have.\n * @param value Maximum number\n *\n * @example\n * ```typespec\n * @maxItems(5)\n * model Endpoints is string[];\n * ```\n */\nextern dec maxItems(target: unknown[] | ModelProperty, value: valueof integer);\n\n/**\n * Specify the minimum value this numeric type should be.\n * @param value Minimum value\n *\n * @example\n * ```typespec\n * @minValue(18)\n * scalar Age is int32;\n * ```\n */\nextern dec minValue(target: numeric | ModelProperty, value: valueof numeric);\n\n/**\n * Specify the maximum value this numeric type should be.\n * @param value Maximum value\n *\n * @example\n * ```typespec\n * @maxValue(200)\n * scalar Age is int32;\n * ```\n */\nextern dec maxValue(target: numeric | ModelProperty, value: valueof numeric);\n\n/**\n * Specify the minimum value this numeric type should be, exclusive of the given\n * value.\n * @param value Minimum value\n *\n * @example\n * ```typespec\n * @minValueExclusive(0)\n * scalar distance is float64;\n * ```\n */\nextern dec minValueExclusive(target: numeric | ModelProperty, value: valueof numeric);\n\n/**\n * Specify the maximum value this numeric type should be, exclusive of the given\n * value.\n * @param value Maximum value\n *\n * @example\n * ```typespec\n * @maxValueExclusive(50)\n * scalar distance is float64;\n * ```\n */\nextern dec maxValueExclusive(target: numeric | ModelProperty, value: valueof numeric);\n\n/**\n * Mark this string as a secret value that should be treated carefully to avoid exposure\n *\n * @example\n * ```typespec\n * @secret\n * scalar Password is string;\n * ```\n */\nextern dec secret(target: string | ModelProperty);\n\n/**\n * Attaches a tag to an operation, interface, or namespace. Multiple `@tag` decorators can be specified to attach multiple tags to a TypeSpec element.\n * @param tag Tag value\n */\nextern dec tag(target: Namespace | Interface | Operation, tag: valueof string);\n\n/**\n * Specifies how a templated type should name their instances.\n * @param name name the template instance should take\n * @param formatArgs Model with key value used to interpolate the name\n *\n * @example\n * ```typespec\n * @friendlyName(\"{name}List\", T)\n * model List<Item> {\n *   value: Item[];\n *   nextLink: string;\n * }\n * ```\n */\nextern dec friendlyName(target: unknown, name: valueof string, formatArgs?: unknown);\n\n/**\n * Provide a set of known values to a string type.\n * @param values Known values enum.\n *\n * @example\n * ```typespec\n * @knownValues(KnownErrorCode)\n * scalar ErrorCode extends string;\n *\n * enum KnownErrorCode {\n *   NotFound,\n *   Invalid,\n * }\n * ```\n */\n#deprecated \"This decorator has been deprecated. Use a named union of string literals with a string variant to achieve the same result without a decorator.\"\nextern dec knownValues(target: string | numeric | ModelProperty, values: Enum);\n\n/**\n * Mark a model property as the key to identify instances of that type\n * @param altName Name of the property. If not specified, the decorated property name is used.\n *\n * @example\n * ```typespec\n * model Pet {\n *   @key id: string;\n * }\n * ```\n */\nextern dec key(target: ModelProperty, altName?: valueof string);\n\n/**\n * Specify this operation is an overload of the given operation.\n * @param overloadbase Base operation that should be a union of all overloads\n *\n * @example\n * ```typespec\n * op upload(data: string | bytes, @header contentType: \"text/plain\" | \"application/octet-stream\"): void;\n * @overload(upload)\n * op uploadString(data: string, @header contentType: \"text/plain\" ): void;\n * @overload(upload)\n * op uploadBytes(data: bytes, @header contentType: \"application/octet-stream\"): void;\n * ```\n */\nextern dec overload(target: Operation, overloadbase: Operation);\n\n/**\n * DEPRECATED: Use `@encodedName` instead.\n *\n * Provide an alternative name for this type.\n * @param targetName Projection target\n * @param projectedName Alternative name\n *\n * @example\n * ```typespec\n * model Certificate {\n *   @projectedName(\"json\", \"exp\")\n *   expireAt: int32;\n * }\n * ```\n */\n#deprecated \"Use `@encodedName` instead for changing the name over the wire.\"\nextern dec projectedName(\n  target: unknown,\n  targetName: valueof string,\n  projectedName: valueof string\n);\n\n/**\n * Provide an alternative name for this type when serialized to the given mime type.\n * @param mimeType Mime type this should apply to. The mime type should be a known mime type as described here https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types without any suffix (e.g. `+json`)\n * @param name Alternative name\n *\n * @example\n *\n * ```typespec\n * model Certificate {\n *   @encodedName(\"application/json\", \"exp\")\n *   @encodedName(\"application/xml\", \"expiry\")\n *   expireAt: int32;\n * }\n * ```\n *\n * @example Invalid values\n *\n * ```typespec\n * @encodedName(\"application/merge-patch+json\", \"exp\")\n *              ^ error cannot use subtype\n * ```\n */\nextern dec encodedName(target: unknown, mimeType: valueof string, name: valueof string);\n\n/**\n * Specify the property to be used to discriminate this type.\n * @param propertyName The property name to use for discrimination\n *\n * @example\n *\n * ```typespec\n * @discriminator(\"kind\")\n * union Pet{ cat: Cat, dog: Dog }\n *\n * model Cat {kind: \"cat\", meow: boolean}\n * model Dog {kind: \"dog\", bark: boolean}\n * ```\n *\n * ```typespec\n * @discriminator(\"kind\")\n * model Pet{ kind: string }\n *\n * model Cat extends Pet {kind: \"cat\", meow: boolean}\n * model Dog extends Pet  {kind: \"dog\", bark: boolean}\n * ```\n */\nextern dec discriminator(target: Model | Union, propertyName: valueof string);\n\n/**\n * Known encoding to use on utcDateTime or offsetDateTime\n */\nenum DateTimeKnownEncoding {\n  /**\n   * RFC 3339 standard. https://www.ietf.org/rfc/rfc3339.txt\n   * Encode to string.\n   */\n  rfc3339: \"rfc3339\",\n\n  /**\n   * RFC 7231 standard. https://www.ietf.org/rfc/rfc7231.txt\n   * Encode to string.\n   */\n  rfc7231: \"rfc7231\",\n\n  /**\n   * Encode a datetime to a unix timestamp.\n   * Unix timestamps are represented as an integer number of seconds since the Unix epoch and usually encoded as an int32.\n   */\n  unixTimestamp: \"unixTimestamp\",\n}\n\n/**\n * Known encoding to use on duration\n */\nenum DurationKnownEncoding {\n  /**\n   * ISO8601 duration\n   */\n  ISO8601: \"ISO8601\",\n\n  /**\n   * Encode to integer or float\n   */\n  seconds: \"seconds\",\n}\n\n/**\n * Known encoding to use on bytes\n */\nenum BytesKnownEncoding {\n  /**\n   * Encode to Base64\n   */\n  base64: \"base64\",\n\n  /**\n   * Encode to Base64 Url\n   */\n  base64url: \"base64url\",\n}\n\n/**\n * Encoding for serializing arrays\n */\nenum ArrayEncoding {\n  /** Each values of the array is separated by a | */\n  pipeDelimited,\n\n  /** Each values of the array is separated by a <space> */\n  spaceDelimited,\n}\n\n/**\n * Specify how to encode the target type.\n * @param encodingOrEncodeAs Known name of an encoding or a scalar type to encode as(Only for numeric types to encode as string).\n * @param encodedAs What target type is this being encoded as. Default to string.\n *\n * @example offsetDateTime encoded with rfc7231\n *\n * ```tsp\n * @encode(\"rfc7231\")\n * scalar myDateTime extends offsetDateTime;\n * ```\n *\n * @example utcDateTime encoded with unixTimestamp\n *\n * ```tsp\n * @encode(\"unixTimestamp\", int32)\n * scalar myDateTime extends unixTimestamp;\n * ```\n *\n * @example encode numeric type to string\n *\n * ```tsp\n * model Pet {\n *   @encode(string) id: int64;\n * }\n * ```\n */\nextern dec encode(\n  target: Scalar | ModelProperty,\n  encodingOrEncodeAs: (valueof string | EnumMember) | Scalar,\n  encodedAs?: Scalar\n);\n\n/** Options for example decorators */\nmodel ExampleOptions {\n  /** The title of the example */\n  title?: string;\n\n  /** Description of the example */\n  description?: string;\n}\n\n/**\n * Provide an example value for a data type.\n *\n * @param example Example value.\n * @param options Optional metadata for the example.\n *\n * @example\n *\n * ```tsp\n * @example(#{name: \"Fluffy\", age: 2})\n * model Pet {\n *  name: string;\n *  age: int32;\n * }\n * ```\n */\nextern dec example(\n  target: Model | Enum | Scalar | Union | ModelProperty | UnionVariant,\n  example: valueof unknown,\n  options?: valueof ExampleOptions\n);\n\n/**\n * Operation example configuration.\n */\nmodel OperationExample {\n  /** Example request body. */\n  parameters?: unknown;\n\n  /** Example response body. */\n  returnType?: unknown;\n}\n\n/**\n * Provide example values for an operation's parameters and corresponding return type.\n *\n * @param example Example value.\n * @param options Optional metadata for the example.\n *\n * @example\n *\n * ```tsp\n * @opExample(#{parameters: #{name: \"Fluffy\", age: 2}, returnType: #{name: \"Fluffy\", age: 2, id: \"abc\"})\n * op createPet(pet: Pet): Pet;\n * ```\n */\nextern dec opExample(\n  target: Operation,\n  example: valueof OperationExample,\n  options?: valueof ExampleOptions\n);\n\n/**\n * Returns the model with required properties removed.\n */\nextern dec withOptionalProperties(target: Model);\n\n/**\n * Returns the model with any default values removed.\n */\nextern dec withoutDefaultValues(target: Model);\n\n/**\n * Returns the model with the given properties omitted.\n * @param omit List of properties to omit\n */\nextern dec withoutOmittedProperties(target: Model, omit: string | Union);\n\n/**\n * Returns the model with only the given properties included.\n * @param pick List of properties to include\n */\nextern dec withPickedProperties(target: Model, pick: string | Union);\n\n//---------------------------------------------------------------------------\n// Paging\n//---------------------------------------------------------------------------\n\n/**\n * Mark this operation as a `list` operation that returns a paginated list of items.\n */\nextern dec list(target: Operation);\n\n/**\n * Pagination property defining the number of items to skip.\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n * }\n * @list op listPets(@offset skip: int32, @pageSize pageSize: int8): Page<Pet>;\n * ```\n */\nextern dec offset(target: ModelProperty);\n\n/**\n * Pagination property defining the page index.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n * }\n * @list op listPets(@pageIndex page: int32, @pageSize pageSize: int8): Page<Pet>;\n * ```\n */\nextern dec pageIndex(target: ModelProperty);\n\n/**\n * Specify the pagination parameter that controls the maximum number of items to include in a page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n * }\n * @list op listPets(@pageIndex page: int32, @pageSize pageSize: int8): Page<Pet>;\n * ```\n */\nextern dec pageSize(target: ModelProperty);\n\n/**\n * Specify the the property that contains the array of page items.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n * }\n * @list op listPets(@pageIndex page: int32, @pageSize pageSize: int8): Page<Pet>;\n * ```\n */\nextern dec pageItems(target: ModelProperty);\n\n/**\n * Pagination property defining the token to get to the next page.\n * It MUST be specified both on the request parameter and the response.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @continuationToken continuationToken: string;\n * }\n * @list op listPets(@continuationToken continuationToken: string): Page<Pet>;\n * ```\n */\nextern dec continuationToken(target: ModelProperty);\n\n/**\n * Pagination property defining a link to the next page.\n *\n * It is expected that navigating to the link will return the same set of responses as the operation that returned the current page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @nextLink next: url;\n *   @prevLink prev: url;\n *   @firstLink first: url;\n *   @lastLink last: url;\n * }\n * @list op listPets(): Page<Pet>;\n * ```\n */\nextern dec nextLink(target: ModelProperty);\n\n/**\n * Pagination property defining a link to the previous page.\n *\n * It is expected that navigating to the link will return the same set of responses as the operation that returned the current page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @nextLink next: url;\n *   @prevLink prev: url;\n *   @firstLink first: url;\n *   @lastLink last: url;\n * }\n * @list op listPets(): Page<Pet>;\n * ```\n */\nextern dec prevLink(target: ModelProperty);\n\n/**\n * Pagination property defining a link to the first page.\n *\n * It is expected that navigating to the link will return the same set of responses as the operation that returned the current page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @nextLink next: url;\n *   @prevLink prev: url;\n *   @firstLink first: url;\n *   @lastLink last: url;\n * }\n * @list op listPets(): Page<Pet>;\n * ```\n */\nextern dec firstLink(target: ModelProperty);\n\n/**\n * Pagination property defining a link to the last page.\n *\n * It is expected that navigating to the link will return the same set of responses as the operation that returned the current page.\n *\n * @example\n * ```tsp\n * model Page<T> {\n *   @pageItems items: T[];\n *   @nextLink next: url;\n *   @prevLink prev: url;\n *   @firstLink first: url;\n *   @lastLink last: url;\n * }\n * @list op listPets(): Page<Pet>;\n * ```\n */\nextern dec lastLink(target: ModelProperty);\n\n//---------------------------------------------------------------------------\n// Debugging\n//---------------------------------------------------------------------------\n\n/**\n * A debugging decorator used to inspect a type.\n * @param text Custom text to log\n */\nextern dec inspectType(target: unknown, text: valueof string);\n\n/**\n * A debugging decorator used to inspect a type name.\n * @param text Custom text to log\n */\nextern dec inspectTypeName(target: unknown, text: valueof string);\n",
  "../compiler/lib/std/reflection.tsp": "namespace TypeSpec.Reflection;\n\nmodel Enum {}\nmodel EnumMember {}\nmodel Interface {}\nmodel Model {}\nmodel ModelProperty {}\nmodel Namespace {}\nmodel Operation {}\nmodel Scalar {}\nmodel Union {}\nmodel UnionVariant {}\nmodel StringTemplate {}\n",
  "../compiler/lib/std/projected-names.tsp": "// Set of projections consuming the @projectedName decorator\n#suppress \"projections-are-experimental\"\nprojection op#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n  }\n}\n\n#suppress \"projections-are-experimental\"\nprojection interface#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n  }\n}\n\n#suppress \"projections-are-experimental\"\nprojection model#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n\n    self::properties::forEach((p) => {\n      if hasProjectedName(p, targetName) {\n        self::renameProperty(p::name, getProjectedName(p, targetName));\n      };\n    });\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n\n    self::projectionBase::properties::forEach((p) => {\n      if hasProjectedName(p, targetName) {\n        self::renameProperty(getProjectedName(p, targetName), p::name);\n      };\n    });\n  }\n}\n\n#suppress \"projections-are-experimental\"\nprojection enum#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n\n    self::members::forEach((p) => {\n      if hasProjectedName(p, targetName) {\n        self::renameMember(p::name, getProjectedName(p, targetName));\n      };\n    });\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n\n    self::projectionBase::members::forEach((p) => {\n      if hasProjectedName(p, targetName) {\n        self::renameMember(getProjectedName(p, targetName), p::name);\n      };\n    });\n  }\n}\n\n#suppress \"projections-are-experimental\"\nprojection union#target {\n  to(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(getProjectedName(self, targetName));\n    };\n  }\n  from(targetName) {\n    if hasProjectedName(self, targetName) {\n      self::rename(self::projectionBase::name);\n    };\n  }\n}\n",
  "../compiler/lib/std/visibility.tsp": "// Copyright (c) Microsoft Corporation\n// Licensed under the MIT license.\n\nimport \"../../dist/src/lib/tsp-index.js\";\n\nusing TypeSpec.Reflection;\n\nnamespace TypeSpec;\n\n/**\n * Indicates that a property is only considered to be present or applicable (\"visible\") with\n * the in the given named contexts (\"visibilities\"). When a property has no visibilities applied\n * to it, it is implicitly visible always.\n *\n * As far as the TypeSpec core library is concerned, visibilities are open-ended and can be arbitrary\n * strings, but  the following visibilities are well-known to standard libraries and should be used\n * with standard emitters that interpret them as follows:\n *\n * - \"read\": output of any operation.\n * - \"create\": input to operations that create an entity..\n * - \"query\": input to operations that read data.\n * - \"update\": input to operations that update data.\n * - \"delete\": input to operations that delete data.\n *\n * See also: [Automatic visibility](https://typespec.io/docs/libraries/http/operations#automatic-visibility)\n *\n * @param visibilities List of visibilities which apply to this property.\n *\n * @example\n *\n * ```typespec\n * model Dog {\n *   // the service will generate an ID, so you don't need to send it.\n *   @visibility(Lifecycle.Read) id: int32;\n *   // the service will store this secret name, but won't ever return it\n *   @visibility(Lifecycle.Create, Lifecycle.Update) secretName: string;\n *   // the regular name is always present\n *   name: string;\n * }\n * ```\n */\nextern dec visibility(target: ModelProperty, ...visibilities: valueof (string | EnumMember)[]);\n\n/**\n * Indicates that a property is not visible in the given visibility class.\n *\n * This decorator removes all active visibility modifiers from the property within\n * the given visibility class.\n *\n * @param visibilityClass The visibility class to make the property invisible within.\n *\n * @example\n * ```typespec\n * model Example {\n *   @invisible(Lifecycle)\n *   hidden_property: string;\n * }\n * ```\n */\nextern dec invisible(target: ModelProperty, visibilityClass: Enum);\n\n/**\n * Removes visibility modifiers from a property.\n *\n * If the visibility modifiers for a visibility class have not been initialized,\n * this decorator will use the default visibility modifiers for the visibility\n * class as the default modifier set.\n *\n * @param target The property to remove visibility from.\n * @param visibilities The visibility modifiers to remove from the target property.\n *\n * @example\n * ```typespec\n * model Example {\n *   // This property will have the Create and Update visibilities, but not the\n *   // Read visibility, since it is removed.\n *   @removeVisibility(Lifecycle.Read)\n *   secret_property: string;\n * }\n * ```\n */\nextern dec removeVisibility(target: ModelProperty, ...visibilities: valueof EnumMember[]);\n\n/**\n * Removes properties that are not considered to be present or applicable\n * (\"visible\") in the given named contexts (\"visibilities\"). Can be used\n * together with spread to effectively spread only visible properties into\n * a new model.\n *\n * See also: [Automatic visibility](https://typespec.io/docs/libraries/http/operations#automatic-visibility)\n *\n * When using an emitter that applies visibility automatically, it is generally\n * not necessary to use this decorator.\n *\n * @param visibilities List of visibilities which apply to this property.\n *\n * @example\n * ```typespec\n * model Dog {\n *   @visibility(\"read\") id: int32;\n *   @visibility(\"create\", \"update\") secretName: string;\n *   name: string;\n * }\n *\n * // The spread operator will copy all the properties of Dog into DogRead,\n * // and @withVisibility will then remove those that are not visible with\n * // create or update visibility.\n * //\n * // In this case, the id property is removed, and the name and secretName\n * // properties are kept.\n * @withVisibility(\"create\", \"update\")\n * model DogCreateOrUpdate {\n *   ...Dog;\n * }\n *\n * // In this case the id and name properties are kept and the secretName property\n * // is removed.\n * @withVisibility(\"read\")\n * model DogRead {\n *   ...Dog;\n * }\n * ```\n */\nextern dec withVisibility(target: Model, ...visibilities: valueof (string | EnumMember)[]);\n\n/**\n * Set the visibility of key properties in a model if not already set.\n *\n * This will set the visibility modifiers of all key properties in the model if the visibility is not already _explicitly_ set,\n * but will not change the visibility of any properties that have visibility set _explicitly_, even if the visibility\n * is the same as the default visibility.\n *\n * Visibility may be explicitly set using any of the following decorators:\n *\n * - `@visibility`\n * - `@removeVisibility`\n * - `@invisible`\n *\n * @param visibility The desired default visibility value. If a key property already has visibility set, it will not be changed.\n */\nextern dec withDefaultKeyVisibility(target: Model, visibility: valueof string | EnumMember);\n\n/**\n * Sets which visibilities apply to parameters for the given operation.\n *\n * @param visibilities List of visibility strings which apply to this operation.\n */\nextern dec parameterVisibility(target: Operation, ...visibilities: valueof (string | EnumMember)[]);\n\n/**\n * Sets which visibilities apply to the return type for the given operation.\n * @param visibilities List of visibility strings which apply to this operation.\n */\nextern dec returnTypeVisibility(\n  target: Operation,\n  ...visibilities: valueof (string | EnumMember)[]\n);\n\n/**\n * Returns the model with non-updateable properties removed.\n */\nextern dec withUpdateableProperties(target: Model);\n\n/**\n * Declares the default visibility modifiers for a visibility class.\n *\n * The default modifiers are used when a property does not have any visibility decorators\n * applied to it.\n *\n * The modifiers passed to this decorator _MUST_ be members of the target Enum.\n *\n * @param visibilities the list of modifiers to use as the default visibility modifiers.\n */\nextern dec defaultVisibility(target: Enum, ...visibilities: valueof EnumMember[]);\n\n/**\n * A visibility class for resource lifecycle phases.\n *\n * These visibilities control whether a property is visible during the create, read, and update phases of a resource's\n * lifecycle.\n *\n * @example\n * ```typespec\n * model Dog {\n *  @visibility(Lifecycle.Read) id: int32;\n *  @visibility(Lifecycle.Create, Lifecycle.Update) secretName: string;\n *  name: string;\n * }\n * ```\n *\n * In this example, the `id` property is only visible during the read phase, and the `secretName` property is only visible\n * during the create and update phases. This means that the server will return the `id` property when returning a `Dog`,\n * but the client will not be able to set or update it. In contrast, the `secretName` property can be set when creating\n * or updating a `Dog`, but the server will never return it. The `name` property has no visibility modifiers and is\n * therefore visible in all phases.\n */\nenum Lifecycle {\n  Create,\n  Read,\n  Update,\n}\n\n/**\n * A visibility filter, used to specify which properties should be included when\n * using the `withVisibilityFilter` decorator.\n *\n * The filter matches any property with ALL of the following:\n * - If the `any` key is present, the property must have at least one of the specified visibilities.\n * - If the `all` key is present, the property must have all of the specified visibilities.\n * - If the `none` key is present, the property must have none of the specified visibilities.\n */\nmodel VisibilityFilter {\n  any?: EnumMember[];\n  all?: EnumMember[];\n  none?: EnumMember[];\n}\n\n/**\n * Applies the given visibility filter to the properties of the target model.\n *\n * This transformation is recursive, so it will also apply the filter to any nested\n * or referenced models that are the types of any properties in the `target`.\n *\n * @param target The model to apply the visibility filter to.\n * @param filter The visibility filter to apply to the properties of the target model.\n *\n * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * @withVisibilityFilter(#{ all: #[Lifecycle.Read] })\n * model DogRead {\n *  ...Dog\n * }\n * ```\n */\nextern dec withVisibilityFilter(target: Model, filter: valueof VisibilityFilter);\n\n/**\n * Transforms the `target` model to include only properties that are visible during the\n * \"Update\" lifecycle phase.\n *\n * Any nested models of optional properties will be transformed into the \"CreateOrUpdate\"\n * lifecycle phase instead of the \"Update\" lifecycle phase, so that nested models may be\n * fully updated.\n *\n * @param target The model to apply the transformation to.\n *\n * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   @visibility(Lifecycle.Create, Lifecycle.Update)\n *   secretName: string;\n *\n *   name: string;\n * }\n *\n * @withLifecycleUpdate\n * model DogUpdate {\n *   ...Dog\n * }\n * ```\n */\nextern dec withLifecycleUpdate(target: Model);\n\n/**\n * A copy of the input model `T` with only the properties that are visible during the\n * \"Create\" resource lifecycle phase.\n *\n * This transformation is recursive, and will include only properties that have the\n * `Lifecycle.Create` visibility modifier.\n *\n * If a `NameTemplate` is provided, the new model will be named according to the template.\n * The template uses the same syntax as the `@friendlyName` decorator.\n *\n * @template T The model to transform.\n * @template NameTemplate The name template to use for the new model.\n *\n *  * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * model CreateDog is Create<Dog>;\n * ```\n */\n@friendlyName(NameTemplate, T)\n@withVisibilityFilter(#{ all: #[Lifecycle.Create] })\nmodel Create<T extends Reflection.Model, NameTemplate extends valueof string = \"Create{name}\"> {\n  ...T;\n}\n\n/**\n * A copy of the input model `T` with only the properties that are visible during the\n * \"Read\" resource lifecycle phase.\n *\n * This transformation is recursive, and will include only properties that have the\n * `Lifecycle.Read` visibility modifier.\n *\n * If a `NameTemplate` is provided, the new model will be named according to the template.\n * The template uses the same syntax as the `@friendlyName` decorator.\n *\n * @template T The model to transform.\n * @template NameTemplate The name template to use for the new model.\n *\n *  * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * model ReadDog is Read<Dog>;\n * ```\n */\n@friendlyName(NameTemplate, T)\n@withVisibilityFilter(#{ all: #[Lifecycle.Read] })\nmodel Read<T extends Reflection.Model, NameTemplate extends valueof string = \"Read{name}\"> {\n  ...T;\n}\n\n/**\n * A copy of the input model `T` with only the properties that are visible during the\n * \"Update\" resource lifecycle phase.\n *\n * This transformation will include only the properties that have the `Lifecycle.Update`\n * visibility modifier, and the types of all properties will be replaced with the\n * equivalent `CreateOrUpdate` transformation.\n *\n * If a `NameTemplate` is provided, the new model will be named according to the template.\n * The template uses the same syntax as the `@friendlyName` decorator.\n *\n * @template T The model to transform.\n * @template NameTemplate The name template to use for the new model.\n *\n *  * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * model UpdateDog is Update<Dog>;\n * ```\n */\n@friendlyName(NameTemplate, T)\n@withLifecycleUpdate\nmodel Update<T extends Reflection.Model, NameTemplate extends valueof string = \"Update{name}\"> {\n  ...T;\n}\n\n/**\n * A copy of the input model `T` with only the properties that are visible during the\n * \"Create\" or \"Update\" resource lifecycle phases.\n *\n * This transformation is recursive, and will include only properties that have the\n * `Lifecycle.Create` or `Lifecycle.Update` visibility modifier.\n *\n * If a `NameTemplate` is provided, the new model will be named according to the template.\n * The template uses the same syntax as the `@friendlyName` decorator.\n *\n * @template T The model to transform.\n * @template NameTemplate The name template to use for the new model.\n *\n *  * @example\n * ```typespec\n * model Dog {\n *   @visibility(Lifecycle.Read)\n *   id: int32;\n *\n *   name: string;\n * }\n *\n * model CreateOrUpdateDog is CreateOrUpdate<Dog>;\n * ```\n */\n@friendlyName(NameTemplate, T)\n@withVisibilityFilter(#{ any: #[Lifecycle.Create, Lifecycle.Update] })\nmodel CreateOrUpdate<\n  T extends Reflection.Model,\n  NameTemplate extends valueof string = \"CreateOrUpdate{name}\"\n> {\n  ...T;\n}\n",
  "lib/proto.tsp": "import \"../dist/src/tsp-index.js\";\n\nnamespace TypeSpec.Protobuf;\n\n/**\n * A model that represents an external Protobuf reference. This type can be used to import and utilize Protobuf\n * declarations that are not declared in TypeSpec within TypeSpec sources. When the emitter encounters an `Extern`, it\n * will insert an `import` statement for the corresponding `Path` and refer to the type by `Name`.\n *\n * #### Usage\n *\n * If you have a file called `test.proto` that declares a package named `test` and a message named `Widget`, you can\n * use the `Extern` type to declare a model in TypeSpec that refers to your external definition of `test.Widget`. See\n * the example below.\n *\n * When the TypeSpec definition of `Widget` is encountered, the Protobuf emitter will represent it as a reference to\n * `test.Widget` and insert an import for it, rather than attempt to convert the model to an equivalent message.\n *\n * @template Path the relative path to a `.proto` file to import\n * @template Name the fully-qualified reference to the type this model represents within the `.proto` file\n *\n * @example\n *\n * ```typespec\n * model Widget is Extern<\"path/to/test.proto\", \"test.Widget\">;\n * ```\n */\n@Private.externRef(Path, Name)\nmodel Extern<Path extends string, Name extends string> {\n  // This _extern property is needed so that getEffectiveModelType will have something to look up. Without it, if an\n  // Extern model is spread into the parameter of an operation, the resulting model is empty and carries no information\n  // that can relate it back to its original definition.\n  _extern: never;\n}\n\n/**\n * Contains some common well-known Protobuf types defined by the google.protobuf library.\n */\nnamespace WellKnown {\n  /**\n   * An empty message.\n   *\n   * This model references `google.protobuf.Empty` from `google/protobuf/empty.proto`.\n   */\n  model Empty is Extern<\"google/protobuf/empty.proto\", \"google.protobuf.Empty\">;\n\n  /**\n   * A timestamp.\n   *\n   * This model references `google.protobuf.Timestamp` from `google/protobuf/timestamp.proto`.\n   */\n  model Timestamp is Extern<\"google/protobuf/timestamp.proto\", \"google.protobuf.Timestamp\">;\n\n  /**\n   * Any value.\n   *\n   * This model references `google.protobuf.Any` from `google/protobuf/any.proto`.\n   */\n  model Any is Extern<\"google/protobuf/any.proto\", \"google.protobuf.Any\">;\n\n  /**\n   * A latitude and longitude.\n   *\n   * This model references `google.type.LatLng` from `google/type/latlng.proto`.\n   */\n  model LatLng is Extern<\"google/type/latlng.proto\", \"google.type.LatLng\">;\n}\n\n/**\n * A signed 32-bit integer that will use the `sint32` encoding when used in a Protobuf message.\n *\n * #### Protobuf binary format\n *\n * Uses variable-length encoding. These more efficiently encode negative numbers than regular int32s.\n */\nscalar sint32 extends int32;\n\n/**\n * A signed 64-bit integer that will use the `sint64` encoding when used in a Protobuf message.\n *\n * #### Protobuf binary format\n *\n * Uses variable-length encoding. These more efficiently encode negative numbers than regular `int64s`.\n */\nscalar sint64 extends int64;\n\n/**\n * A signed 32-bit integer that will use the `sfixed32` encoding when used in a Protobuf message.\n *\n * #### Protobuf binary format\n *\n * Always four bytes.\n */\nscalar sfixed32 extends int32;\n\n/**\n * A signed 64-bit integer that will use the `sfixed64` encoding when used in a Protobuf message.\n *\n * #### Protobuf binary format\n *\n * Always eight bytes.\n */\nscalar sfixed64 extends int64;\n\n/**\n * An unsigned 32-bit integer that will use the `fixed32` encoding when used in a Protobuf message.\n *\n * #### Protobuf binary format\n *\n * Always four bytes. More efficient than `uint32` if values are often greater than 2<sup>28</sup>.\n */\nscalar fixed32 extends uint32;\n\n/**\n * An unsigned 64-bit integer that will use the `fixed64` encoding when used in a Protobuf message.\n *\n * #### Protobuf binary format\n *\n * Always eight bytes. More efficient than `uint64` if values are often greater than 2<sup>56</sup>.\n */\nscalar fixed64 extends uint64;\n\n/**\n * Types recognized as \"integral\" types\n */\nalias integral = int32 | int64 | uint32 | uint64 | boolean;\n\n/**\n * A type representing a Protobuf `map`. Instances of this type in models will be converted to the built-in `map` type\n * in Protobuf.\n *\n * The key type of a Protobuf `map` must be any integral type or `string`. The value type can be any type other than\n * another `Map`.\n *\n * @template Key the key type (any integral type or string)\n * @template Value the value type (any type other than another map)\n */\n@Private._map\nmodel Map<Key extends integral | string, Value> {}\n\n/**\n * Declares that a model is a Protobuf message.\n *\n * Messages can be detected automatically if either of the following two conditions are met:\n *\n * - The model has a `@field` annotation on all of its properties.\n * - The model is referenced by any service operation.\n *\n * This decorator will force the emitter to check and emit a model.\n */\nextern dec message(target: {});\n\n/**\n * Defines the field index of a model property for conversion to a Protobuf\n * message.\n *\n * The field index of a Protobuf message must:\n *   - fall between 1 and 2<sup>29</sup> - 1, inclusive.\n *   - not fall within the implementation reserved range of 19000 to 19999, inclusive.\n *   - not fall within any range that was [marked reserved](#@TypeSpec.Protobuf.reserve).\n *\n * #### API Compatibility Note\n *\n * Fields are accessed by index, so changing the index of a field is an API breaking change.\n *\n * #### Encoding\n *\n * Field indices between 1 and 15 are encoded using a single byte, while field indices from 16 through 2047 require two\n * bytes, so those indices between 1 and 15 should be preferred and reserved for elements that are frequently or always\n * set in the message. See the [Protobuf binary format](https://protobuf.dev/programming-guides/encoding/).\n *\n * @param index The whole-number index of the field.\n *\n * @example\n *\n * ```typespec\n * model ExampleMessage {\n *   @field(1)\n *   test: string;\n * }\n * ```\n */\nextern dec field(target: TypeSpec.Reflection.ModelProperty, index: valueof uint32);\n\n/**\n * Reserve a field index, range, or name. If a field definition collides with a reservation, the emitter will produce\n * an error.\n *\n * This decorator accepts multiple reservations. Each reservation is one of the following:\n *\n * - a `string`, in which case the reservation refers to a field name.\n * - a `uint32`, in which case the reservation refers to a field index.\n * - a tuple `[uint32, uint32]`, in which case the reservation refers to a field range that is _inclusive_ of both ends.\n *\n * Unlike in Protobuf, where field name and index reservations must be separated, you can mix string and numeric field\n * reservations in a single `@reserve` call in TypeSpec.\n *\n * #### API Compatibility Note\n *\n * Field reservations prevent users of your Protobuf specification from using the given field names or indices. This can\n * be useful if a field is removed, as it will further prevent adding a new, incompatible field and will prevent users\n * from utilizing the field index at runtime in a way that may break compatibility with users of older specifications.\n *\n * See _[Protobuf Language Guide - Reserved Fields](https://protobuf.dev/programming-guides/proto3/#reserved)_ for more\n * information.\n *\n * @param reservations a list of field reservations\n *\n * @example\n *\n * ```typespec\n * // Reserve the fields 8-15 inclusive, 100, and the field name \"test\" within a model.\n * @reserve([8, 15], 100, \"test\")\n * model Example {\n *   // ...\n * }\n * ```\n */\nextern dec reserve(target: {}, ...reservations: valueof (string | [uint32, uint32] | uint32)[]);\n\n/**\n * Declares that a TypeSpec interface constitutes a Protobuf service. The contents of the interface will be converted to\n * a `service` declaration in the resulting Protobuf file.\n */\nextern dec service(target: TypeSpec.Reflection.Interface);\n\n// FIXME: cannot link to the package decorator directly because it is detected as a broken link.\n/**\n * Details applied to a package definition by the [`@package`](./decorators#@TypeSpec.Protobuf.package) decorator.\n */\nmodel PackageDetails {\n  /**\n   * The package's name.\n   *\n   * By default, the package's name is constructed from the namespace it is applied to.\n   */\n  name?: string;\n\n  /**\n   * The package's top-level options.\n   *\n   * See the [Protobuf Language Guide - Options](https://protobuf.dev/programming-guides/proto3/#options) for more information.\n   *\n   * Currently, only string, boolean, and numeric options are supported.\n   */\n  options?: Record<string | boolean | numeric>;\n}\n\n/**\n * Declares that a TypeSpec namespace constitutes a Protobuf package. The contents of the namespace will be emitted to a\n * single Protobuf file.\n *\n * @param details the optional details of the package\n */\nextern dec package(target: TypeSpec.Reflection.Namespace, details?: PackageDetails);\n\n/**\n * The streaming mode of an operation. One of:\n *\n * - `Duplex`: both the input and output of the operation are streaming.\n * - `In`: the input of the operation is streaming.\n * - `Out`: the output of the operation is streaming.\n * - `None`: neither the input nor the output are streaming.\n *\n * See the [`@stream`](./decorators#@TypeSpec.Protobuf.stream) decorator.\n */\nenum StreamMode {\n  /**\n   * Both the input and output of the operation are streaming. Both the client and service will stream messages to each\n   * other until the connections are closed.\n   */\n  Duplex,\n\n  /**\n   * The input of the operation is streaming. The client will send a stream of events; and, once the stream is closed,\n   * the service will respond with a message.\n   */\n  In,\n\n  /**\n   * The output of the operation is streaming. The client will send a message to the service, and the service will send\n   * a stream of events back to the client.\n   */\n  Out,\n\n  /**\n   * Neither the input nor the output are streaming. This is the default mode of an operation without the `@stream`\n   * decorator.\n   */\n  None,\n}\n\n/**\n * Set the streaming mode of an operation. See [StreamMode](./data-types#TypeSpec.Protobuf.StreamMode) for more information.\n *\n * @param mode The streaming mode to apply to this operation.\n *\n * @example\n *\n * ```typespec\n * @stream(StreamMode.Out)\n * op logs(...LogsRequest): LogEvent;\n * ```\n *\n * @example\n *\n * ```typespec\n * @stream(StreamMode.Duplex)\n * op connectToMessageService(...Message): Message;\n * ```\n */\nextern dec stream(target: TypeSpec.Reflection.Operation, mode: StreamMode);\n\nnamespace Private {\n  extern dec externRef(target: Reflection.Model, path: string, name: string);\n  extern dec _map(target: Reflection.Model);\n}\n"
};
const _TypeSpecLibrary_ = {
  jsSourceFiles: TypeSpecJSSources,
  typespecSourceFiles: TypeSpecSources,
};

export { $_map, $decorators, $externRef, $field, $lib, $message, $onEmit, $onValidate, $package, $reserve, $service, $stream, PROTO_FULL_IDENT, _TypeSpecLibrary_, isMap, namespace };
