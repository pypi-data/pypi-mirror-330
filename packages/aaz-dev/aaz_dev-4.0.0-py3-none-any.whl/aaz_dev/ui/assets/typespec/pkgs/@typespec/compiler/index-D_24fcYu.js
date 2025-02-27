import { b as getAnyExtensionFromPath, n as normalizePath, j as joinPaths, g as getDirectoryPath, u as isUrl, i as isPathAbsolute, r as resolvePath } from './path-utils-3cuVtir1.js';

function createSourceFile(text, path) {
    let lineStarts = undefined;
    return {
        text,
        path,
        getLineStarts,
        getLineAndCharacterOfPosition,
    };
    function getLineStarts() {
        return (lineStarts = lineStarts ?? scanLineStarts(text));
    }
    function getLineAndCharacterOfPosition(position) {
        const starts = getLineStarts();
        let line = binarySearch(starts, position);
        // When binarySearch returns < 0 indicating that the value was not found, it
        // returns the bitwise complement of the index where the value would need to
        // be inserted to keep the array sorted. So flipping the bits back to this
        // positive index tells us what the line number would be if we were to
        // create a new line starting at the given position, and subtracting 1 from
        // that therefore gives us the line number we're after.
        if (line < 0) {
            line = ~line - 1;
        }
        return {
            line,
            character: position - starts[line],
        };
    }
}
function getSourceFileKindFromExt(path) {
    const ext = getAnyExtensionFromPath(path);
    if (ext === ".js" || ext === ".mjs") {
        return "js";
    }
    else if (ext === ".tsp" || ext === ".cadl") {
        return "typespec";
    }
    else {
        return undefined;
    }
}
function scanLineStarts(text) {
    const starts = [];
    let start = 0;
    let pos = 0;
    while (pos < text.length) {
        const ch = text.charCodeAt(pos);
        pos++;
        switch (ch) {
            case 13 /* CharCode.CarriageReturn */:
                if (text.charCodeAt(pos) === 10 /* CharCode.LineFeed */) {
                    pos++;
                }
            // fallthrough
            case 10 /* CharCode.LineFeed */:
                starts.push(start);
                start = pos;
                break;
        }
    }
    starts.push(start);
    return starts;
}
/**
 * Search sorted array of numbers for the given value. If found, return index
 * in array where value was found. If not found, return a negative number that
 * is the bitwise complement of the index where value would need to be inserted
 * to keep the array sorted.
 */
function binarySearch(array, value) {
    let low = 0;
    let high = array.length - 1;
    while (low <= high) {
        const middle = low + ((high - low) >> 1);
        const v = array[middle];
        if (v < value) {
            low = middle + 1;
        }
        else if (v > value) {
            high = middle - 1;
        }
        else {
            return middle;
        }
    }
    return ~low;
}

var ResolutionResultFlags;
(function (ResolutionResultFlags) {
    ResolutionResultFlags[ResolutionResultFlags["None"] = 0] = "None";
    ResolutionResultFlags[ResolutionResultFlags["Resolved"] = 2] = "Resolved";
    ResolutionResultFlags[ResolutionResultFlags["Unknown"] = 4] = "Unknown";
    ResolutionResultFlags[ResolutionResultFlags["Ambiguous"] = 8] = "Ambiguous";
    ResolutionResultFlags[ResolutionResultFlags["NotFound"] = 16] = "NotFound";
    ResolutionResultFlags[ResolutionResultFlags["ResolutionFailed"] = 28] = "ResolutionFailed";
})(ResolutionResultFlags || (ResolutionResultFlags = {}));
/**
 * AST types
 */
var SyntaxKind;
(function (SyntaxKind) {
    SyntaxKind[SyntaxKind["TypeSpecScript"] = 0] = "TypeSpecScript";
    /** @deprecated Use TypeSpecScript */
    SyntaxKind[SyntaxKind["CadlScript"] = 0] = "CadlScript";
    SyntaxKind[SyntaxKind["JsSourceFile"] = 1] = "JsSourceFile";
    SyntaxKind[SyntaxKind["ImportStatement"] = 2] = "ImportStatement";
    SyntaxKind[SyntaxKind["Identifier"] = 3] = "Identifier";
    SyntaxKind[SyntaxKind["AugmentDecoratorStatement"] = 4] = "AugmentDecoratorStatement";
    SyntaxKind[SyntaxKind["DecoratorExpression"] = 5] = "DecoratorExpression";
    SyntaxKind[SyntaxKind["DirectiveExpression"] = 6] = "DirectiveExpression";
    SyntaxKind[SyntaxKind["MemberExpression"] = 7] = "MemberExpression";
    SyntaxKind[SyntaxKind["NamespaceStatement"] = 8] = "NamespaceStatement";
    SyntaxKind[SyntaxKind["UsingStatement"] = 9] = "UsingStatement";
    SyntaxKind[SyntaxKind["OperationStatement"] = 10] = "OperationStatement";
    SyntaxKind[SyntaxKind["OperationSignatureDeclaration"] = 11] = "OperationSignatureDeclaration";
    SyntaxKind[SyntaxKind["OperationSignatureReference"] = 12] = "OperationSignatureReference";
    SyntaxKind[SyntaxKind["ModelStatement"] = 13] = "ModelStatement";
    SyntaxKind[SyntaxKind["ModelExpression"] = 14] = "ModelExpression";
    SyntaxKind[SyntaxKind["ModelProperty"] = 15] = "ModelProperty";
    SyntaxKind[SyntaxKind["ModelSpreadProperty"] = 16] = "ModelSpreadProperty";
    SyntaxKind[SyntaxKind["ScalarStatement"] = 17] = "ScalarStatement";
    SyntaxKind[SyntaxKind["InterfaceStatement"] = 18] = "InterfaceStatement";
    SyntaxKind[SyntaxKind["UnionStatement"] = 19] = "UnionStatement";
    SyntaxKind[SyntaxKind["UnionVariant"] = 20] = "UnionVariant";
    SyntaxKind[SyntaxKind["EnumStatement"] = 21] = "EnumStatement";
    SyntaxKind[SyntaxKind["EnumMember"] = 22] = "EnumMember";
    SyntaxKind[SyntaxKind["EnumSpreadMember"] = 23] = "EnumSpreadMember";
    SyntaxKind[SyntaxKind["AliasStatement"] = 24] = "AliasStatement";
    SyntaxKind[SyntaxKind["DecoratorDeclarationStatement"] = 25] = "DecoratorDeclarationStatement";
    SyntaxKind[SyntaxKind["FunctionDeclarationStatement"] = 26] = "FunctionDeclarationStatement";
    SyntaxKind[SyntaxKind["FunctionParameter"] = 27] = "FunctionParameter";
    SyntaxKind[SyntaxKind["UnionExpression"] = 28] = "UnionExpression";
    SyntaxKind[SyntaxKind["IntersectionExpression"] = 29] = "IntersectionExpression";
    SyntaxKind[SyntaxKind["TupleExpression"] = 30] = "TupleExpression";
    SyntaxKind[SyntaxKind["ArrayExpression"] = 31] = "ArrayExpression";
    SyntaxKind[SyntaxKind["StringLiteral"] = 32] = "StringLiteral";
    SyntaxKind[SyntaxKind["NumericLiteral"] = 33] = "NumericLiteral";
    SyntaxKind[SyntaxKind["BooleanLiteral"] = 34] = "BooleanLiteral";
    SyntaxKind[SyntaxKind["StringTemplateExpression"] = 35] = "StringTemplateExpression";
    SyntaxKind[SyntaxKind["StringTemplateHead"] = 36] = "StringTemplateHead";
    SyntaxKind[SyntaxKind["StringTemplateMiddle"] = 37] = "StringTemplateMiddle";
    SyntaxKind[SyntaxKind["StringTemplateTail"] = 38] = "StringTemplateTail";
    SyntaxKind[SyntaxKind["StringTemplateSpan"] = 39] = "StringTemplateSpan";
    SyntaxKind[SyntaxKind["ExternKeyword"] = 40] = "ExternKeyword";
    SyntaxKind[SyntaxKind["VoidKeyword"] = 41] = "VoidKeyword";
    SyntaxKind[SyntaxKind["NeverKeyword"] = 42] = "NeverKeyword";
    SyntaxKind[SyntaxKind["UnknownKeyword"] = 43] = "UnknownKeyword";
    SyntaxKind[SyntaxKind["ValueOfExpression"] = 44] = "ValueOfExpression";
    SyntaxKind[SyntaxKind["TypeReference"] = 45] = "TypeReference";
    SyntaxKind[SyntaxKind["ProjectionReference"] = 46] = "ProjectionReference";
    SyntaxKind[SyntaxKind["TemplateParameterDeclaration"] = 47] = "TemplateParameterDeclaration";
    SyntaxKind[SyntaxKind["EmptyStatement"] = 48] = "EmptyStatement";
    SyntaxKind[SyntaxKind["InvalidStatement"] = 49] = "InvalidStatement";
    SyntaxKind[SyntaxKind["LineComment"] = 50] = "LineComment";
    SyntaxKind[SyntaxKind["BlockComment"] = 51] = "BlockComment";
    SyntaxKind[SyntaxKind["Doc"] = 52] = "Doc";
    SyntaxKind[SyntaxKind["DocText"] = 53] = "DocText";
    SyntaxKind[SyntaxKind["DocParamTag"] = 54] = "DocParamTag";
    SyntaxKind[SyntaxKind["DocPropTag"] = 55] = "DocPropTag";
    SyntaxKind[SyntaxKind["DocReturnsTag"] = 56] = "DocReturnsTag";
    SyntaxKind[SyntaxKind["DocErrorsTag"] = 57] = "DocErrorsTag";
    SyntaxKind[SyntaxKind["DocTemplateTag"] = 58] = "DocTemplateTag";
    SyntaxKind[SyntaxKind["DocUnknownTag"] = 59] = "DocUnknownTag";
    SyntaxKind[SyntaxKind["Projection"] = 60] = "Projection";
    SyntaxKind[SyntaxKind["ProjectionParameterDeclaration"] = 61] = "ProjectionParameterDeclaration";
    SyntaxKind[SyntaxKind["ProjectionModelSelector"] = 62] = "ProjectionModelSelector";
    SyntaxKind[SyntaxKind["ProjectionModelPropertySelector"] = 63] = "ProjectionModelPropertySelector";
    SyntaxKind[SyntaxKind["ProjectionScalarSelector"] = 64] = "ProjectionScalarSelector";
    SyntaxKind[SyntaxKind["ProjectionOperationSelector"] = 65] = "ProjectionOperationSelector";
    SyntaxKind[SyntaxKind["ProjectionUnionSelector"] = 66] = "ProjectionUnionSelector";
    SyntaxKind[SyntaxKind["ProjectionUnionVariantSelector"] = 67] = "ProjectionUnionVariantSelector";
    SyntaxKind[SyntaxKind["ProjectionInterfaceSelector"] = 68] = "ProjectionInterfaceSelector";
    SyntaxKind[SyntaxKind["ProjectionEnumSelector"] = 69] = "ProjectionEnumSelector";
    SyntaxKind[SyntaxKind["ProjectionEnumMemberSelector"] = 70] = "ProjectionEnumMemberSelector";
    SyntaxKind[SyntaxKind["ProjectionExpressionStatement"] = 71] = "ProjectionExpressionStatement";
    SyntaxKind[SyntaxKind["ProjectionIfExpression"] = 72] = "ProjectionIfExpression";
    SyntaxKind[SyntaxKind["ProjectionBlockExpression"] = 73] = "ProjectionBlockExpression";
    SyntaxKind[SyntaxKind["ProjectionMemberExpression"] = 74] = "ProjectionMemberExpression";
    SyntaxKind[SyntaxKind["ProjectionLogicalExpression"] = 75] = "ProjectionLogicalExpression";
    SyntaxKind[SyntaxKind["ProjectionEqualityExpression"] = 76] = "ProjectionEqualityExpression";
    SyntaxKind[SyntaxKind["ProjectionUnaryExpression"] = 77] = "ProjectionUnaryExpression";
    SyntaxKind[SyntaxKind["ProjectionRelationalExpression"] = 78] = "ProjectionRelationalExpression";
    SyntaxKind[SyntaxKind["ProjectionArithmeticExpression"] = 79] = "ProjectionArithmeticExpression";
    SyntaxKind[SyntaxKind["ProjectionCallExpression"] = 80] = "ProjectionCallExpression";
    SyntaxKind[SyntaxKind["ProjectionLambdaExpression"] = 81] = "ProjectionLambdaExpression";
    SyntaxKind[SyntaxKind["ProjectionLambdaParameterDeclaration"] = 82] = "ProjectionLambdaParameterDeclaration";
    SyntaxKind[SyntaxKind["ProjectionModelExpression"] = 83] = "ProjectionModelExpression";
    SyntaxKind[SyntaxKind["ProjectionModelProperty"] = 84] = "ProjectionModelProperty";
    SyntaxKind[SyntaxKind["ProjectionModelSpreadProperty"] = 85] = "ProjectionModelSpreadProperty";
    SyntaxKind[SyntaxKind["ProjectionSpreadProperty"] = 86] = "ProjectionSpreadProperty";
    SyntaxKind[SyntaxKind["ProjectionTupleExpression"] = 87] = "ProjectionTupleExpression";
    SyntaxKind[SyntaxKind["ProjectionStatement"] = 88] = "ProjectionStatement";
    SyntaxKind[SyntaxKind["ProjectionDecoratorReferenceExpression"] = 89] = "ProjectionDecoratorReferenceExpression";
    SyntaxKind[SyntaxKind["Return"] = 90] = "Return";
    SyntaxKind[SyntaxKind["JsNamespaceDeclaration"] = 91] = "JsNamespaceDeclaration";
    SyntaxKind[SyntaxKind["TemplateArgument"] = 92] = "TemplateArgument";
    SyntaxKind[SyntaxKind["TypeOfExpression"] = 93] = "TypeOfExpression";
    SyntaxKind[SyntaxKind["ObjectLiteral"] = 94] = "ObjectLiteral";
    SyntaxKind[SyntaxKind["ObjectLiteralProperty"] = 95] = "ObjectLiteralProperty";
    SyntaxKind[SyntaxKind["ObjectLiteralSpreadProperty"] = 96] = "ObjectLiteralSpreadProperty";
    SyntaxKind[SyntaxKind["ArrayLiteral"] = 97] = "ArrayLiteral";
    SyntaxKind[SyntaxKind["ConstStatement"] = 98] = "ConstStatement";
    SyntaxKind[SyntaxKind["CallExpression"] = 99] = "CallExpression";
    SyntaxKind[SyntaxKind["ScalarConstructor"] = 100] = "ScalarConstructor";
})(SyntaxKind || (SyntaxKind = {}));
var IdentifierKind;
(function (IdentifierKind) {
    IdentifierKind[IdentifierKind["TypeReference"] = 0] = "TypeReference";
    IdentifierKind[IdentifierKind["TemplateArgument"] = 1] = "TemplateArgument";
    IdentifierKind[IdentifierKind["Decorator"] = 2] = "Decorator";
    IdentifierKind[IdentifierKind["Function"] = 3] = "Function";
    IdentifierKind[IdentifierKind["Using"] = 4] = "Using";
    IdentifierKind[IdentifierKind["Declaration"] = 5] = "Declaration";
    IdentifierKind[IdentifierKind["ModelExpressionProperty"] = 6] = "ModelExpressionProperty";
    IdentifierKind[IdentifierKind["ModelStatementProperty"] = 7] = "ModelStatementProperty";
    IdentifierKind[IdentifierKind["ObjectLiteralProperty"] = 8] = "ObjectLiteralProperty";
    IdentifierKind[IdentifierKind["Other"] = 9] = "Other";
})(IdentifierKind || (IdentifierKind = {}));
/** Used to explicitly specify that a diagnostic has no target. */
const NoTarget = Symbol.for("NoTarget");
var ListenerFlow;
(function (ListenerFlow) {
    /**
     * Do not navigate any containing or referenced type.
     */
    ListenerFlow[ListenerFlow["NoRecursion"] = 1] = "NoRecursion";
})(ListenerFlow || (ListenerFlow = {}));

let manifest;
try {
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    manifest = (await import('./manifest-CyOCC6aZ.js')).default;
}
catch {
    const name = "../dist/manifest.js";
    manifest = (await import(/* @vite-ignore */ /* webpackIgnore: true */ name)).default;
}
const typespecVersion = manifest.version;
/** @deprecated Use typespecVersion */
const cadlVersion = typespecVersion;
const MANIFEST = manifest;

/**
 * Recursively calls Object.freeze such that all objects and arrays
 * referenced are frozen.
 *
 * Does not support cycles. Intended to be used only on plain data that can
 * be directly represented in JSON.
 */
function deepFreeze(value) {
    if (Array.isArray(value)) {
        value.forEach(deepFreeze);
    }
    else if (typeof value === "object") {
        for (const prop in value) {
            deepFreeze(value[prop]);
        }
    }
    return Object.freeze(value);
}
/**
 * Deeply clones an object.
 *
 * Does not support cycles. Intended to be used only on plain data that can
 * be directly represented in JSON.
 */
function deepClone(value) {
    if (Array.isArray(value)) {
        return value.map(deepClone);
    }
    if (typeof value === "object") {
        const obj = {};
        for (const prop in value) {
            obj[prop] = deepClone(value[prop]);
        }
        return obj;
    }
    return value;
}
/**
 * Checks if two objects are deeply equal.
 *
 * Does not support cycles. Intended to be used only on plain data that can
 * be directly represented in JSON.
 */
function deepEquals(left, right) {
    if (left === right) {
        return true;
    }
    if (left === null || right === null || typeof left !== "object" || typeof right !== "object") {
        return false;
    }
    if (Array.isArray(left)) {
        return Array.isArray(right) ? arrayEquals(left, right, deepEquals) : false;
    }
    return mapEquals(new Map(Object.entries(left)), new Map(Object.entries(right)), deepEquals);
}
/**
 * Check if two arrays have the same elements.
 *
 * @param equals Optional callback for element equality comparison.
 *               Default is to compare by identity using `===`.
 */
function arrayEquals(left, right, equals = (x, y) => x === y) {
    if (left === right) {
        return true;
    }
    if (left.length !== right.length) {
        return false;
    }
    for (let i = 0; i < left.length; i++) {
        if (!equals(left[i], right[i])) {
            return false;
        }
    }
    return true;
}
/**
 * Check if two maps have the same entries.
 *
 * @param equals Optional callback for value equality comparison.
 *               Default is to compare by identity using `===`.
 */
function mapEquals(left, right, equals = (x, y) => x === y) {
    if (left === right) {
        return true;
    }
    if (left.size !== right.size) {
        return false;
    }
    for (const [key, value] of left) {
        if (!right.has(key) || !equals(value, right.get(key))) {
            return false;
        }
    }
    return true;
}
async function getNormalizedRealPath(host, path) {
    try {
        return normalizePath(await host.realpath(path));
    }
    catch (error) {
        // This could mean the file got deleted but VSCode still has it in memory. So keep the original path.
        if (error.code === "ENOENT") {
            return normalizePath(path);
        }
        throw error;
    }
}
async function doIO(action, path, reportDiagnostic, options) {
    let result;
    try {
        result = await action(path);
    }
    catch (e) {
        let diagnostic;
        let target = options?.diagnosticTarget ?? NoTarget;
        // blame the JS file, not the TypeSpec import statement for JS syntax errors.
        if (e instanceof SyntaxError && options?.jsDiagnosticTarget) {
            target = options.jsDiagnosticTarget;
        }
        switch (e.code) {
            case "ENOENT":
                if (options?.allowFileNotFound) {
                    return undefined;
                }
                diagnostic = createDiagnostic({ code: "file-not-found", target, format: { path } });
                break;
            default:
                diagnostic = createDiagnostic({
                    code: "file-load",
                    target,
                    format: { message: e.message },
                });
                break;
        }
        reportDiagnostic(diagnostic);
        return undefined;
    }
    return result;
}
async function loadFile(host, path, load, reportDiagnostic, options) {
    const file = await doIO(host.readFile, path, reportDiagnostic, options);
    if (!file) {
        return [undefined, createSourceFile("", path)];
    }
    let data;
    try {
        data = load(file.text);
    }
    catch (e) {
        reportDiagnostic({
            code: "file-load",
            message: e.message,
            severity: "error",
            target: { file, pos: 1, end: 1 },
        });
        return [undefined, file];
    }
    return [data, file];
}
async function readUrlOrPath(host, pathOrUrl) {
    if (isUrl(pathOrUrl)) {
        return host.readUrl(pathOrUrl);
    }
    return host.readFile(pathOrUrl);
}
function resolveRelativeUrlOrPath(base, relativeOrAbsolute) {
    if (isUrl(relativeOrAbsolute)) {
        return relativeOrAbsolute;
    }
    else if (isPathAbsolute(relativeOrAbsolute)) {
        return relativeOrAbsolute;
    }
    else if (isUrl(base)) {
        return new URL(relativeOrAbsolute, base).href;
    }
    else {
        return resolvePath(base, relativeOrAbsolute);
    }
}
/**
 * A specially typed version of `Array.isArray` to work around [this issue](https://github.com/microsoft/TypeScript/issues/17002).
 */
function isArray(arg) {
    return Array.isArray(arg);
}
/**
 * Check if argument is not undefined.
 */
function isDefined(arg) {
    return arg !== undefined;
}
function isWhitespaceStringOrUndefined(str) {
    return !str || /^\s*$/.test(str);
}
function firstNonWhitespaceCharacterIndex(line) {
    return line.search(/\S/);
}
function distinctArray(arr, keySelector) {
    const map = new Map();
    for (const item of arr) {
        map.set(keySelector(item), item);
    }
    return Array.from(map.values());
}
function tryParseJson(content) {
    try {
        return JSON.parse(content);
    }
    catch {
        return undefined;
    }
}
/**
 * Remove undefined properties from object.
 */
function omitUndefined(data) {
    return Object.fromEntries(Object.entries(data).filter(([k, v]) => v !== undefined));
}
/**
 * Look for the project root by looking up until a `package.json` is found.
 * @param path Path to start looking
 * @param lookIn
 */
async function findProjectRoot(statFn, path) {
    let current = path;
    while (true) {
        const pkgPath = joinPaths(current, "package.json");
        const stat = await doIO(() => statFn(pkgPath), pkgPath, () => { });
        if (stat?.isFile()) {
            return current;
        }
        const parent = getDirectoryPath(current);
        if (parent === current) {
            return undefined;
        }
        current = parent;
    }
}
/**
 * Extract package.json's tspMain entry point in a given path. Note, it takes into
 * back compat for deprecated cadlMain
 * @param path Path that contains package.json
 * @param reportDiagnostic optional diagnostic handler.
 */
function resolveTspMain(packageJson) {
    if (packageJson?.tspMain !== undefined) {
        return packageJson.tspMain;
    }
    if (packageJson?.cadlMain !== undefined) {
        return packageJson.cadlMain;
    }
    return undefined;
}
/**
 * A map keyed by a set of objects.
 *
 * This is likely non-optimal.
 */
class MultiKeyMap {
    #currentId = 0;
    #idMap = new WeakMap();
    #items = new Map();
    get(items) {
        return this.#items.get(this.compositeKeyFor(items));
    }
    set(items, value) {
        const key = this.compositeKeyFor(items);
        this.#items.set(key, value);
    }
    compositeKeyFor(items) {
        return items.map((i) => this.keyFor(i)).join(",");
    }
    keyFor(item) {
        if (this.#idMap.has(item)) {
            return this.#idMap.get(item);
        }
        const id = this.#currentId++;
        this.#idMap.set(item, id);
        return id;
    }
}
/**
 * A map with exactly two keys per value.
 *
 * Functionally the same as `MultiKeyMap<[K1, K2], V>`, but more efficient.
 * @hidden bug in typedoc
 */
class TwoLevelMap extends Map {
    /**
     * Get an existing entry in the map or add a new one if not found.
     *
     * @param key1 The first key
     * @param key2 The second key
     * @param create A callback to create the new entry when not found.
     * @param sentinel An optional sentinel value to use to indicate that the
     *                 entry is being created.
     */
    getOrAdd(key1, key2, create, sentinel) {
        let map = this.get(key1);
        if (map === undefined) {
            map = new Map();
            this.set(key1, map);
        }
        let entry = map.get(key2);
        if (entry === undefined) {
            if (sentinel !== undefined) {
                map.set(key2, sentinel);
            }
            entry = create();
            map.set(key2, entry);
        }
        return entry;
    }
}
// Adapted from https://github.com/microsoft/TypeScript/blob/bc52ff6f4be9347981de415a35da90497eae84ac/src/compiler/core.ts#L1507
class Queue {
    #elements;
    #headIndex = 0;
    constructor(elements) {
        this.#elements = elements?.slice() ?? [];
    }
    isEmpty() {
        return this.#headIndex === this.#elements.length;
    }
    enqueue(...items) {
        this.#elements.push(...items);
    }
    dequeue() {
        if (this.isEmpty()) {
            throw new Error("Queue is empty.");
        }
        const result = this.#elements[this.#headIndex];
        this.#elements[this.#headIndex] = undefined; // Don't keep referencing dequeued item
        this.#headIndex++;
        // If more than half of the queue is empty, copy the remaining elements to the
        // front and shrink the array (unless we'd be saving fewer than 100 slots)
        if (this.#headIndex > 100 && this.#headIndex > this.#elements.length >> 1) {
            const newLength = this.#elements.length - this.#headIndex;
            this.#elements.copyWithin(0, this.#headIndex);
            this.#elements.length = newLength;
            this.#headIndex = 0;
        }
        return result;
    }
}
/**
 * Casts away readonly typing.
 *
 * Use it like this when it is safe to override readonly typing:
 *   mutate(item).prop = value;
 */
function mutate(value) {
    return value;
}
function createRekeyableMap(entries) {
    return new RekeyableMapImpl(entries);
}
class RekeyableMapImpl {
    #keys = new Map();
    #values = new Map();
    constructor(entries) {
        if (entries) {
            for (const [key, value] of entries) {
                this.set(key, value);
            }
        }
    }
    clear() {
        this.#keys.clear();
        this.#values.clear();
    }
    delete(key) {
        const keyItem = this.#keys.get(key);
        if (keyItem) {
            this.#keys.delete(key);
            return this.#values.delete(keyItem);
        }
        return false;
    }
    forEach(callbackfn, thisArg) {
        this.#values.forEach((value, keyItem) => {
            callbackfn(value, keyItem.key, this);
        }, thisArg);
    }
    get(key) {
        const keyItem = this.#keys.get(key);
        return keyItem ? this.#values.get(keyItem) : undefined;
    }
    has(key) {
        return this.#keys.has(key);
    }
    set(key, value) {
        let keyItem = this.#keys.get(key);
        if (!keyItem) {
            keyItem = { key };
            this.#keys.set(key, keyItem);
        }
        this.#values.set(keyItem, value);
        return this;
    }
    get size() {
        return this.#values.size;
    }
    *entries() {
        for (const [k, v] of this.#values) {
            yield [k.key, v];
        }
    }
    *keys() {
        for (const k of this.#values.keys()) {
            yield k.key;
        }
    }
    values() {
        return this.#values.values();
    }
    [Symbol.iterator]() {
        return this.entries();
    }
    [Symbol.toStringTag] = "RekeyableMap";
    rekey(existingKey, newKey) {
        const keyItem = this.#keys.get(existingKey);
        if (!keyItem) {
            return false;
        }
        this.#keys.delete(existingKey);
        const newKeyItem = this.#keys.get(newKey);
        if (newKeyItem) {
            this.#values.delete(newKeyItem);
        }
        keyItem.key = newKey;
        this.#keys.set(newKey, keyItem);
        return true;
    }
}

/**
 * Create a new diagnostics creator.
 * @param diagnostics Map of the potential diagnostics.
 * @param libraryName Optional name of the library if in the scope of a library.
 * @returns @see DiagnosticCreator
 */
function createDiagnosticCreator(diagnostics, libraryName) {
    const errorMessage = libraryName
        ? `It must match one of the code defined in the library '${libraryName}'`
        : "It must match one of the code defined in the compiler.";
    function createDiagnostic(diagnostic) {
        const diagnosticDef = diagnostics[diagnostic.code];
        if (!diagnosticDef) {
            const codeStr = Object.keys(diagnostics)
                .map((x) => ` - ${x}`)
                .join("\n");
            const code = String(diagnostic.code);
            throw new Error(`Unexpected diagnostic code '${code}'. ${errorMessage}. Defined codes:\n${codeStr}`);
        }
        const message = diagnosticDef.messages[diagnostic.messageId ?? "default"];
        if (!message) {
            const codeStr = Object.keys(diagnosticDef.messages)
                .map((x) => ` - ${x}`)
                .join("\n");
            const messageId = String(diagnostic.messageId);
            const code = String(diagnostic.code);
            throw new Error(`Unexpected message id '${messageId}'. ${errorMessage} for code '${code}'. Defined codes:\n${codeStr}`);
        }
        const messageStr = typeof message === "string" ? message : message(diagnostic.format);
        const result = {
            code: libraryName ? `${libraryName}/${String(diagnostic.code)}` : diagnostic.code.toString(),
            severity: diagnosticDef.severity,
            message: messageStr,
            target: diagnostic.target,
        };
        if (diagnosticDef.url) {
            mutate(result).url = diagnosticDef.url;
        }
        if (diagnostic.codefixes) {
            mutate(result).codefixes = diagnostic.codefixes;
        }
        return result;
    }
    function reportDiagnostic(program, diagnostic) {
        const diag = createDiagnostic(diagnostic);
        program.reportDiagnostic(diag);
    }
    return {
        diagnostics,
        createDiagnostic,
        reportDiagnostic,
    };
}

function paramMessage(strings, ...keys) {
    const template = (dict) => {
        const result = [strings[0]];
        keys.forEach((key, i) => {
            const value = dict[key];
            if (value !== undefined) {
                result.push(value);
            }
            result.push(strings[i + 1]);
        });
        return result.join("");
    };
    template.keys = keys;
    return template;
}

// Static assert: this won't compile if one of the entries above is invalid.
const diagnostics = {
    /**
     * Scanner errors.
     */
    "digit-expected": {
        severity: "error",
        messages: {
            default: "Digit expected.",
        },
    },
    "hex-digit-expected": {
        severity: "error",
        messages: {
            default: "Hexadecimal digit expected.",
        },
    },
    "binary-digit-expected": {
        severity: "error",
        messages: {
            default: "Binary digit expected.",
        },
    },
    unterminated: {
        severity: "error",
        messages: {
            default: paramMessage `Unterminated ${"token"}.`,
        },
    },
    "creating-file": {
        severity: "error",
        messages: {
            default: paramMessage `Error creating single file: ${"filename"},  ${"error"}`,
        },
    },
    "invalid-escape-sequence": {
        severity: "error",
        messages: {
            default: "Invalid escape sequence.",
        },
    },
    "no-new-line-start-triple-quote": {
        severity: "error",
        messages: {
            default: "String content in triple quotes must begin on a new line.",
        },
    },
    "no-new-line-end-triple-quote": {
        severity: "error",
        messages: {
            default: "Closing triple quotes must begin on a new line.",
        },
    },
    "triple-quote-indent": {
        severity: "error",
        description: "Report when a triple-quoted string has lines with less indentation as the closing triple quotes.",
        url: "https://typespec.io/docs/standard-library/diags/triple-quote-indent",
        messages: {
            default: "All lines in triple-quoted string lines must have the same indentation as closing triple quotes.",
        },
    },
    "invalid-character": {
        severity: "error",
        messages: {
            default: "Invalid character.",
        },
    },
    /**
     * Utils
     */
    "file-not-found": {
        severity: "error",
        messages: {
            default: paramMessage `File ${"path"} not found.`,
        },
    },
    "file-load": {
        severity: "error",
        messages: {
            default: paramMessage `${"message"}`,
        },
    },
    /**
     * Init templates
     */
    "init-template-invalid-json": {
        severity: "error",
        messages: {
            default: paramMessage `Unable to parse ${"url"}: ${"message"}. Check that the template URL is correct.`,
        },
    },
    "init-template-download-failed": {
        severity: "error",
        messages: {
            default: paramMessage `Failed to download template from ${"url"}: ${"message"}. Check that the template URL is correct.`,
        },
    },
    /**
     * Parser errors.
     */
    "multiple-blockless-namespace": {
        severity: "error",
        messages: {
            default: "Cannot use multiple blockless namespaces.",
        },
    },
    "blockless-namespace-first": {
        severity: "error",
        messages: {
            default: "Blockless namespaces can't follow other declarations.",
            topLevel: "Blockless namespace can only be top-level.",
        },
    },
    "import-first": {
        severity: "error",
        messages: {
            default: "Imports must come prior to namespaces or other declarations.",
            topLevel: "Imports must be top-level and come prior to namespaces or other declarations.",
        },
    },
    "token-expected": {
        severity: "error",
        messages: {
            default: paramMessage `${"token"} expected.`,
            unexpected: paramMessage `Unexpected token ${"token"}`,
            numericOrStringLiteral: "Expected numeric or string literal.",
            identifier: "Identifier expected.",
            projectionDirection: "from or to expected.",
            expression: "Expression expected.",
            statement: "Statement expected.",
            property: "Property expected.",
            enumMember: "Enum member expected.",
            typeofTarget: "Typeof expects a value literal or value reference.",
        },
    },
    "unknown-directive": {
        severity: "error",
        messages: {
            default: paramMessage `Unknown directive '#${"id"}'`,
        },
    },
    "augment-decorator-target": {
        severity: "error",
        messages: {
            default: `Augment decorator first argument must be a type reference.`,
            noInstance: `Cannot reference template instances`,
        },
    },
    "duplicate-decorator": {
        severity: "warning",
        messages: {
            default: paramMessage `Decorator ${"decoratorName"} cannot be used twice on the same declaration.`,
        },
    },
    "decorator-conflict": {
        severity: "warning",
        messages: {
            default: paramMessage `Decorator ${"decoratorName"} cannot be used with decorator ${"otherDecoratorName"} on the same declaration.`,
        },
    },
    "reserved-identifier": {
        severity: "error",
        messages: {
            default: "Keyword cannot be used as identifier.",
        },
    },
    "invalid-directive-location": {
        severity: "error",
        messages: {
            default: paramMessage `Cannot place directive on ${"nodeName"}.`,
        },
    },
    "invalid-decorator-location": {
        severity: "error",
        messages: {
            default: paramMessage `Cannot decorate ${"nodeName"}.`,
        },
    },
    "invalid-projection": {
        severity: "error",
        messages: {
            default: "Invalid projection",
            wrongType: "Non-projection can't be used to project",
            noTo: "Projection missing to projection",
            projectionError: paramMessage `An error occurred when projecting this type: ${"message"}`,
        },
    },
    "default-required": {
        severity: "error",
        messages: {
            default: "Required template parameters must not follow optional template parameters",
        },
    },
    "invalid-template-argument-name": {
        severity: "error",
        messages: {
            default: "Template parameter argument names must be valid, bare identifiers.",
        },
    },
    "invalid-template-default": {
        severity: "error",
        messages: {
            default: "Template parameter defaults can only reference previously declared type parameters.",
        },
    },
    "required-parameter-first": {
        severity: "error",
        messages: {
            default: "A required parameter cannot follow an optional parameter.",
        },
    },
    "rest-parameter-last": {
        severity: "error",
        messages: {
            default: "A rest parameter must be last in a parameter list.",
        },
    },
    "rest-parameter-required": {
        severity: "error",
        messages: {
            default: "A rest parameter cannot be optional.",
        },
    },
    /**
     * Parser doc comment warnings.
     * Design goal: Malformed doc comments should only produce warnings, not errors.
     */
    "doc-invalid-identifier": {
        severity: "warning",
        messages: {
            default: "Invalid identifier.",
            tag: "Invalid tag name. Use backticks around code if this was not meant to be a tag.",
            param: "Invalid parameter name.",
            prop: "Invalid property name.",
            templateParam: "Invalid template parameter name.",
        },
    },
    /**
     * Checker
     */
    "using-invalid-ref": {
        severity: "error",
        messages: {
            default: "Using must refer to a namespace",
        },
    },
    "invalid-type-ref": {
        severity: "error",
        messages: {
            default: "Invalid type reference",
            decorator: "Can't put a decorator in a type",
            function: "Can't use a function as a type",
        },
    },
    "invalid-template-args": {
        severity: "error",
        messages: {
            default: "Invalid template arguments.",
            notTemplate: "Can't pass template arguments to non-templated type",
            tooMany: "Too many template arguments provided.",
            unknownName: paramMessage `No parameter named '${"name"}' exists in the target template.`,
            positionalAfterNamed: "Positional template arguments cannot follow named arguments in the same argument list.",
            missing: paramMessage `Template argument '${"name"}' is required and not specified.`,
            specifiedAgain: paramMessage `Cannot specify template argument '${"name"}' again.`,
        },
    },
    "intersect-non-model": {
        severity: "error",
        messages: {
            default: "Cannot intersect non-model types (including union types).",
        },
    },
    "intersect-invalid-index": {
        severity: "error",
        messages: {
            default: "Cannot intersect incompatible models.",
            never: "Cannot intersect a model that cannot hold properties.",
            array: "Cannot intersect an array model.",
        },
    },
    "incompatible-indexer": {
        severity: "error",
        messages: {
            default: paramMessage `Property is incompatible with indexer:\n${"message"}`,
        },
    },
    "no-array-properties": {
        severity: "error",
        messages: {
            default: "Array models cannot have any properties.",
        },
    },
    "intersect-duplicate-property": {
        severity: "error",
        messages: {
            default: paramMessage `Intersection contains duplicate property definitions for ${"propName"}`,
        },
    },
    "invalid-decorator": {
        severity: "error",
        messages: {
            default: paramMessage `${"id"} is not a decorator`,
        },
    },
    "invalid-ref": {
        severity: "error",
        messages: {
            default: paramMessage `Cannot resolve ${"id"}`,
            identifier: paramMessage `Unknown identifier ${"id"}`,
            decorator: paramMessage `Unknown decorator @${"id"}`,
            inDecorator: paramMessage `Cannot resolve ${"id"} in decorator`,
            underNamespace: paramMessage `Namespace ${"namespace"} doesn't have member ${"id"}`,
            member: paramMessage `${"kind"} doesn't have member ${"id"}`,
            metaProperty: paramMessage `${"kind"} doesn't have meta property ${"id"}`,
            node: paramMessage `Cannot resolve '${"id"}' in node ${"nodeName"} since it has no members. Did you mean to use "::" instead of "."?`,
        },
    },
    "duplicate-property": {
        severity: "error",
        messages: {
            default: paramMessage `Model already has a property named ${"propName"}`,
        },
    },
    "override-property-mismatch": {
        severity: "error",
        messages: {
            default: paramMessage `Model has an inherited property named ${"propName"} of type ${"propType"} which cannot override type ${"parentType"}`,
            disallowedOptionalOverride: paramMessage `Model has a required inherited property named ${"propName"} which cannot be overridden as optional`,
        },
    },
    "extend-scalar": {
        severity: "error",
        messages: {
            default: "Scalar must extend other scalars.",
        },
    },
    "extend-model": {
        severity: "error",
        messages: {
            default: "Models must extend other models.",
            modelExpression: "Models cannot extend model expressions.",
        },
    },
    "is-model": {
        severity: "error",
        messages: {
            default: "Model `is` must specify another model.",
            modelExpression: "Model `is` cannot specify a model expression.",
        },
    },
    "is-operation": {
        severity: "error",
        messages: {
            default: "Operation can only reuse the signature of another operation.",
        },
    },
    "spread-model": {
        severity: "error",
        messages: {
            default: "Cannot spread properties of non-model type.",
            neverIndex: "Cannot spread type because it cannot hold properties.",
            selfSpread: "Cannot spread type within its own declaration.",
        },
    },
    "unsupported-default": {
        severity: "error",
        messages: {
            default: paramMessage `Default must be have a value type but has type '${"type"}'.`,
        },
    },
    "spread-object": {
        severity: "error",
        messages: {
            default: "Cannot spread properties of non-object type.",
        },
    },
    "expect-value": {
        severity: "error",
        messages: {
            default: paramMessage `${"name"} refers to a type, but is being used as a value here.`,
            model: paramMessage `${"name"} refers to a model type, but is being used as a value here. Use #{} to create an object value.`,
            tuple: paramMessage `${"name"} refers to a tuple type, but is being used as a value here. Use #[] to create an array value.`,
            templateConstraint: paramMessage `${"name"} template parameter can be a type but is being used as a value here.`,
        },
    },
    "non-callable": {
        severity: "error",
        messages: {
            default: paramMessage `Type ${"type"} is not is not callable.`,
        },
    },
    "named-init-required": {
        severity: "error",
        messages: {
            default: paramMessage `Only scalar deriving from 'string', 'numeric' or 'boolean' can be instantited without a named constructor.`,
        },
    },
    "invalid-primitive-init": {
        severity: "error",
        messages: {
            default: `Instantiating scalar deriving from 'string', 'numeric' or 'boolean' can only take a single argument.`,
            invalidArg: paramMessage `Expected a single argument of type ${"expected"} but got ${"actual"}.`,
        },
    },
    "ambiguous-scalar-type": {
        severity: "error",
        messages: {
            default: paramMessage `Value ${"value"} type is ambiguous between ${"types"}. To resolve be explicit when instantiating this value(e.g. '${"example"}(${"value"})').`,
        },
    },
    unassignable: {
        severity: "error",
        messages: {
            default: paramMessage `Type '${"sourceType"}' is not assignable to type '${"targetType"}'`,
        },
    },
    "property-unassignable": {
        severity: "error",
        messages: {
            default: paramMessage `Types of property '${"propName"}' are incompatible`,
        },
    },
    "property-required": {
        severity: "error",
        messages: {
            default: paramMessage `Property '${"propName"}' is required in type '${"targetType"}' but here is optional.`,
        },
    },
    "value-in-type": {
        severity: "error",
        messages: {
            default: "A value cannot be used as a type.",
            referenceTemplate: "Template parameter can be passed values but is used as a type.",
            noTemplateConstraint: "Template parameter has no constraint but a value is passed. Add `extends valueof unknown` to accept any value.",
        },
    },
    "no-prop": {
        severity: "error",
        messages: {
            default: paramMessage `Property '${"propName"}' cannot be defined because model cannot hold properties.`,
        },
    },
    "missing-index": {
        severity: "error",
        messages: {
            default: paramMessage `Index signature for type '${"indexType"}' is missing in type '${"sourceType"}'.`,
        },
    },
    "missing-property": {
        severity: "error",
        messages: {
            default: paramMessage `Property '${"propertyName"}' is missing on type '${"sourceType"}' but required in '${"targetType"}'`,
        },
    },
    "unexpected-property": {
        severity: "error",
        messages: {
            default: paramMessage `Object value may only specify known properties, and '${"propertyName"}' does not exist in type '${"type"}'.`,
        },
    },
    "extends-interface": {
        severity: "error",
        messages: {
            default: "Interfaces can only extend other interfaces",
        },
    },
    "extends-interface-duplicate": {
        severity: "error",
        messages: {
            default: paramMessage `Interface extends cannot have duplicate members. The duplicate member is named ${"name"}`,
        },
    },
    "interface-duplicate": {
        severity: "error",
        messages: {
            default: paramMessage `Interface already has a member named ${"name"}`,
        },
    },
    "union-duplicate": {
        severity: "error",
        messages: {
            default: paramMessage `Union already has a variant named ${"name"}`,
        },
    },
    "enum-member-duplicate": {
        severity: "error",
        messages: {
            default: paramMessage `Enum already has a member named ${"name"}`,
        },
    },
    "constructor-duplicate": {
        severity: "error",
        messages: {
            default: paramMessage `A constructor already exists with name ${"name"}`,
        },
    },
    "spread-enum": {
        severity: "error",
        messages: {
            default: "Cannot spread members of non-enum type.",
        },
    },
    "decorator-fail": {
        severity: "error",
        messages: {
            default: paramMessage `Decorator ${"decoratorName"} failed!\n\n${"error"}`,
        },
    },
    "rest-parameter-array": {
        severity: "error",
        messages: {
            default: "A rest parameter must be of an array type.",
        },
    },
    "decorator-extern": {
        severity: "error",
        messages: {
            default: "A decorator declaration must be prefixed with the 'extern' modifier.",
        },
    },
    "function-extern": {
        severity: "error",
        messages: {
            default: "A function declaration must be prefixed with the 'extern' modifier.",
        },
    },
    "missing-implementation": {
        severity: "error",
        messages: {
            default: "Extern declaration must have an implementation in JS file.",
        },
    },
    "overload-same-parent": {
        severity: "error",
        messages: {
            default: `Overload must be in the same interface or namespace.`,
        },
    },
    shadow: {
        severity: "warning",
        messages: {
            default: paramMessage `Shadowing parent template parameter with the same name "${"name"}"`,
        },
    },
    "invalid-deprecation-argument": {
        severity: "error",
        messages: {
            default: paramMessage `#deprecation directive is expecting a string literal as the message but got a "${"kind"}"`,
            missing: "#deprecation directive is expecting a message argument but none was provided.",
        },
    },
    "duplicate-deprecation": {
        severity: "warning",
        messages: {
            default: "The #deprecated directive cannot be used more than once on the same declaration.",
        },
    },
    /**
     * Configuration
     */
    "config-invalid-argument": {
        severity: "error",
        messages: {
            default: paramMessage `Argument "${"name"}" is not defined as a parameter in the config.`,
        },
    },
    "config-circular-variable": {
        severity: "error",
        messages: {
            default: paramMessage `There is a circular reference to variable "${"name"}" in the cli configuration or arguments.`,
        },
    },
    "config-path-absolute": {
        severity: "error",
        messages: {
            default: paramMessage `Path "${"path"}" cannot be relative. Use {cwd} or {project-root} to specify what the path should be relative to.`,
        },
    },
    "config-invalid-name": {
        severity: "error",
        messages: {
            default: paramMessage `The configuration name "${"name"}" is invalid because it contains a dot ("."). Using a dot will conflict with using nested configuration values.`,
        },
    },
    "path-unix-style": {
        severity: "warning",
        messages: {
            default: paramMessage `Path should use unix style separators. Use "/" instead of "\\".`,
        },
    },
    "config-path-not-found": {
        severity: "error",
        messages: {
            default: paramMessage `No configuration file found at config path "${"path"}".`,
        },
    },
    /**
     * Program
     */
    "dynamic-import": {
        severity: "error",
        messages: {
            default: "Dynamically generated TypeSpec cannot have imports",
        },
    },
    "invalid-import": {
        severity: "error",
        messages: {
            default: "Import paths must reference either a directory, a .tsp file, or .js file",
        },
    },
    "invalid-main": {
        severity: "error",
        messages: {
            default: "Main file must either be a .tsp file or a .js file.",
        },
    },
    "import-not-found": {
        severity: "error",
        messages: {
            default: paramMessage `Couldn't resolve import "${"path"}"`,
        },
    },
    "library-invalid": {
        severity: "error",
        messages: {
            default: paramMessage `Library "${"path"}" is invalid: ${"message"}`,
        },
    },
    "incompatible-library": {
        severity: "warning",
        messages: {
            default: paramMessage `Multiple versions of "${"name"}" library were loaded:\n${"versionMap"}`,
        },
    },
    "compiler-version-mismatch": {
        severity: "warning",
        messages: {
            default: paramMessage `Current TypeSpec compiler conflicts with local version of @typespec/compiler referenced in ${"basedir"}. \nIf this warning occurs on the command line, try running \`typespec\` with a working directory of ${"basedir"}. \nIf this warning occurs in the IDE, try configuring the \`tsp-server\` path to ${"betterTypeSpecServerPath"}.\n  Expected: ${"expected"}\n  Resolved: ${"actual"}`,
        },
    },
    "duplicate-symbol": {
        severity: "error",
        messages: {
            default: paramMessage `Duplicate name: "${"name"}"`,
        },
    },
    "decorator-decl-target": {
        severity: "error",
        messages: {
            default: "dec must have at least one parameter.",
            required: "dec first parameter must be required.",
        },
    },
    "projections-are-experimental": {
        severity: "warning",
        messages: {
            default: "Projections are experimental - your code will need to change as this feature evolves.",
        },
    },
    "mixed-string-template": {
        severity: "error",
        messages: {
            default: "String template is interpolating values and types. It must be either all values to produce a string value or or all types for string template type.",
        },
    },
    "non-literal-string-template": {
        severity: "error",
        messages: {
            default: "Value interpolated in this string template cannot be converted to a string. Only literal types can be automatically interpolated.",
        },
    },
    /**
     * Binder
     */
    "ambiguous-symbol": {
        severity: "error",
        messages: {
            default: paramMessage `"${"name"}" is an ambiguous name between ${"duplicateNames"}. Try using fully qualified name instead: ${"duplicateNames"}`,
        },
    },
    "duplicate-using": {
        severity: "error",
        messages: {
            default: paramMessage `duplicate using of "${"usingName"}" namespace`,
        },
    },
    /**
     * Library
     */
    "on-validate-fail": {
        severity: "error",
        messages: {
            default: paramMessage `onValidate failed with errors. ${"error"}`,
        },
    },
    "invalid-emitter": {
        severity: "error",
        messages: {
            default: paramMessage `Requested emitter package ${"emitterPackage"} does not provide an "$onEmit" function.`,
        },
    },
    "js-error": {
        severity: "error",
        messages: {
            default: paramMessage `Failed to load ${"specifier"} due to the following JS error: ${"error"}`,
        },
    },
    "missing-import": {
        severity: "error",
        messages: {
            default: paramMessage `Emitter '${"emitterName"}' requires '${"requiredImport"}' to be imported. Add 'import "${"requiredImport"}".`,
        },
    },
    /**
     * Linter
     */
    "invalid-rule-ref": {
        severity: "error",
        messages: {
            default: paramMessage `Reference "${"ref"}" is not a valid reference to a rule or ruleset. It must be in the following format: "<library-name>:<rule-name>"`,
        },
    },
    "unknown-rule": {
        severity: "error",
        messages: {
            default: paramMessage `Rule "${"ruleName"}" is not found in library "${"libraryName"}"`,
        },
    },
    "unknown-rule-set": {
        severity: "error",
        messages: {
            default: paramMessage `Rule set "${"ruleSetName"}" is not found in library "${"libraryName"}"`,
        },
    },
    "rule-enabled-disabled": {
        severity: "error",
        messages: {
            default: paramMessage `Rule "${"ruleName"}" has been enabled and disabled in the same ruleset.`,
        },
    },
    /**
     * Formatter
     */
    "format-failed": {
        severity: "error",
        messages: {
            default: paramMessage `File '${"file"}' failed to format. ${"details"}`,
        },
    },
    /**
     * Decorator
     */
    "invalid-pattern-regex": {
        severity: "warning",
        messages: {
            default: "@pattern decorator expects a valid regular expression pattern.",
        },
    },
    "decorator-wrong-target": {
        severity: "error",
        messages: {
            default: paramMessage `Cannot apply ${"decorator"} decorator to ${"to"}`,
            withExpected: paramMessage `Cannot apply ${"decorator"} decorator to ${"to"} since it is not assignable to ${"expected"}`,
        },
    },
    "invalid-argument": {
        severity: "error",
        messages: {
            default: paramMessage `Argument of type '${"value"}' is not assignable to parameter of type '${"expected"}'`,
        },
    },
    "invalid-argument-count": {
        severity: "error",
        messages: {
            default: paramMessage `Expected ${"expected"} arguments, but got ${"actual"}.`,
            atLeast: paramMessage `Expected at least ${"expected"} arguments, but got ${"actual"}.`,
        },
    },
    "known-values-invalid-enum": {
        severity: "error",
        messages: {
            default: paramMessage `Enum cannot be used on this type. Member ${"member"} is not assignable to type ${"type"}.`,
        },
    },
    "invalid-value": {
        severity: "error",
        messages: {
            default: paramMessage `Type '${"kind"}' is not a value type.`,
            atPath: paramMessage `Type '${"kind"}' of '${"path"}' is not a value type.`,
        },
    },
    deprecated: {
        severity: "warning",
        messages: {
            default: paramMessage `Deprecated: ${"message"}`,
        },
    },
    "no-optional-key": {
        severity: "error",
        messages: {
            default: paramMessage `Property '${"propertyName"}' marked as key cannot be optional.`,
        },
    },
    "invalid-discriminated-union": {
        severity: "error",
        messages: {
            default: "",
            noAnonVariants: "Unions with anonymous variants cannot be discriminated",
        },
    },
    "invalid-discriminated-union-variant": {
        severity: "error",
        messages: {
            default: paramMessage `Union variant "${"name"}" must be a model type.`,
            noDiscriminant: paramMessage `Variant "${"name"}" type is missing the discriminant property "${"discriminant"}".`,
            wrongDiscriminantType: paramMessage `Variant "${"name"}" type's discriminant property "${"discriminant"}" must be a string literal or string enum member.`,
        },
    },
    "missing-discriminator-property": {
        severity: "error",
        messages: {
            default: paramMessage `Each derived model of a discriminated model type should have set the discriminator property("${"discriminator"}") or have a derived model which has. Add \`${"discriminator"}: "<discriminator-value>"\``,
        },
    },
    "invalid-discriminator-value": {
        severity: "error",
        messages: {
            default: paramMessage `Discriminator value should be a string, union of string or string enum but was ${"kind"}.`,
            required: "The discriminator property must be a required property.",
            duplicate: paramMessage `Discriminator value "${"discriminator"}" is already used in another variant.`,
        },
    },
    "invalid-encode": {
        severity: "error",
        messages: {
            default: "Invalid encoding",
            wrongType: paramMessage `Encoding '${"encoding"}' cannot be used on type '${"type"}'. Expected: ${"expected"}.`,
            wrongEncodingType: paramMessage `Encoding '${"encoding"}' on type '${"type"}' is expected to be serialized as '${"expected"}' but got '${"actual"}'.`,
            wrongNumericEncodingType: paramMessage `Encoding '${"encoding"}' on type '${"type"}' is expected to be serialized as '${"expected"}' but got '${"actual"}'. Set '@encode' 2nd parameter to be of type ${"expected"}. e.g. '@encode("${"encoding"}", int32)'`,
            firstArg: `First argument of "@encode" must be the encoding name or the string type when encoding numeric types.`,
        },
    },
    "invalid-mime-type": {
        severity: "error",
        messages: {
            default: paramMessage `Invalid mime type '${"mimeType"}'`,
        },
    },
    "no-mime-type-suffix": {
        severity: "error",
        messages: {
            default: paramMessage `Cannot use mime type '${"mimeType"}' with suffix '${"suffix"}'. Use a simple mime \`type/subtype\` instead.`,
        },
    },
    "encoded-name-conflict": {
        severity: "error",
        messages: {
            default: paramMessage `Encoded name '${"name"}' conflicts with existing member name for mime type '${"mimeType"}'`,
            duplicate: paramMessage `Same encoded name '${"name"}' is used for 2 members '${"mimeType"}'`,
        },
    },
    "incompatible-paging-props": {
        severity: "error",
        messages: {
            default: paramMessage `Paging property has multiple types: '${"kinds"}'`,
        },
    },
    "invalid-paging-prop": {
        severity: "error",
        messages: {
            default: paramMessage `Paging property '${"kind"}' is not valid in this context.`,
            input: paramMessage `Paging property '${"kind"}' cannot be used in the parameters of an operation.`,
            output: paramMessage `Paging property '${"kind"}' cannot be used in the return type of an operation.`,
        },
    },
    "duplicate-paging-prop": {
        severity: "error",
        messages: {
            default: paramMessage `Duplicate property paging '${"kind"}' for operation ${"operationName"}.`,
        },
    },
    "missing-paging-items": {
        severity: "error",
        messages: {
            default: paramMessage `Paged operation '${"operationName"}' return type must have a property annotated with @pageItems.`,
        },
    },
    /**
     * Service
     */
    "service-decorator-duplicate": {
        severity: "error",
        messages: {
            default: `@service can only be set once per TypeSpec document.`,
        },
    },
    "list-type-not-model": {
        severity: "error",
        messages: {
            default: "@list decorator's parameter must be a model type.",
        },
    },
    "invalid-range": {
        severity: "error",
        messages: {
            default: paramMessage `Range "${"start"}..${"end"}" is invalid.`,
        },
    },
    /**
     * Mutator
     */
    "add-response": {
        severity: "error",
        messages: {
            default: "Cannot add a response to anything except an operation statement.",
        },
    },
    "add-parameter": {
        severity: "error",
        messages: {
            default: "Cannot add a parameter to anything except an operation statement.",
        },
    },
    "add-model-property": {
        severity: "error",
        messages: {
            default: "Cannot add a model property to anything except a model statement.",
        },
    },
    "add-model-property-fail": {
        severity: "error",
        messages: {
            default: paramMessage `Could not add property/parameter "${"propertyName"}" of type "${"propertyTypeName"}"`,
        },
    },
    "add-response-type": {
        severity: "error",
        messages: {
            default: paramMessage `Could not add response type "${"responseTypeName"}" to operation ${"operationName"}"`,
        },
    },
    "circular-base-type": {
        severity: "error",
        messages: {
            default: paramMessage `Type '${"typeName"}' recursively references itself as a base type.`,
        },
    },
    "circular-constraint": {
        severity: "error",
        messages: {
            default: paramMessage `Type parameter '${"typeName"}' has a circular constraint.`,
        },
    },
    "circular-op-signature": {
        severity: "error",
        messages: {
            default: paramMessage `Operation '${"typeName"}' recursively references itself.`,
        },
    },
    "circular-alias-type": {
        severity: "error",
        messages: {
            default: paramMessage `Alias type '${"typeName"}' recursively references itself.`,
        },
    },
    "circular-const": {
        severity: "error",
        messages: {
            default: paramMessage `const '${"name"}' recursively references itself.`,
        },
    },
    "circular-prop": {
        severity: "error",
        messages: {
            default: paramMessage `Property '${"propName"}' recursively references itself.`,
        },
    },
    "conflict-marker": {
        severity: "error",
        messages: {
            default: "Conflict marker encountered.",
        },
    },
    // #region Visibility
    "visibility-sealed": {
        severity: "error",
        messages: {
            default: paramMessage `Visibility of property '${"propName"}' is sealed and cannot be changed.`,
        },
    },
    "visibility-mixed-legacy": {
        severity: "error",
        messages: {
            default: "Cannot apply both string (legacy) visibility modifiers and enum-based visibility modifiers to a property.",
        },
    },
    "default-visibility-not-member": {
        severity: "error",
        messages: {
            default: "The default visibility modifiers of a class must be members of the class enum.",
        },
    },
    // #endregion
    // #region CLI
    "no-compatible-vs-installed": {
        severity: "error",
        messages: {
            default: "No compatible version of Visual Studio found.",
        },
    },
    "vs-extension-windows-only": {
        severity: "error",
        messages: {
            default: "Visual Studio extension is not supported on non-Windows.",
        },
    },
    "vscode-in-path": {
        severity: "error",
        messages: {
            default: "Couldn't find VS Code 'code' command in PATH. Make sure you have the VS Code executable added to the system PATH.",
            osx: "Couldn't find VS Code 'code' command in PATH. Make sure you have the VS Code executable added to the system PATH.\nSee instruction for Mac OS here https://code.visualstudio.com/docs/setup/mac",
        },
    },
    // #endregion CLI
};
const { createDiagnostic, reportDiagnostic } = createDiagnosticCreator(diagnostics);

/**
 * Helper class to track duplicate instance
 */
class DuplicateTracker {
    #entries = new Map();
    /**
     * Track usage of K.
     * @param k key that is being checked for duplicate.
     * @param v value that map to the key
     */
    track(k, v) {
        const existing = this.#entries.get(k);
        if (existing === undefined) {
            this.#entries.set(k, [v]);
        }
        else {
            existing.push(v);
        }
    }
    /**
     * Return iterator of all the duplicate entries.
     */
    *entries() {
        for (const [k, v] of this.#entries.entries()) {
            if (v.length > 1) {
                yield [k, v];
            }
        }
    }
}

export { paramMessage as A, MultiKeyMap as B, createDiagnosticCreator as C, DuplicateTracker as D, IdentifierKind as I, ListenerFlow as L, MANIFEST as M, NoTarget as N, Queue as Q, ResolutionResultFlags as R, SyntaxKind as S, TwoLevelMap as T, deepClone as a, createDiagnostic as b, createSourceFile as c, deepFreeze as d, doIO as e, resolveTspMain as f, createRekeyableMap as g, deepEquals as h, mapEquals as i, findProjectRoot as j, isDefined as k, loadFile as l, mutate as m, isArray as n, omitUndefined as o, readUrlOrPath as p, resolveRelativeUrlOrPath as q, reportDiagnostic as r, getNormalizedRealPath as s, distinctArray as t, isWhitespaceStringOrUndefined as u, tryParseJson as v, firstNonWhitespaceCharacterIndex as w, typespecVersion as x, getSourceFileKindFromExt as y, cadlVersion as z };
