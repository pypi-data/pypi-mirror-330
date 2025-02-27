import { r as resolvePath, j as joinPaths, n as normalizePath, g as getDirectoryPath } from './path-utils-3cuVtir1.js';

function createBaseErrorMsg(importSpecifier) {
    return `Could not resolve import "${importSpecifier}" `;
}
function createErrorMsg(context, reason, isImports) {
    const { specifier, packageUrl } = context;
    const base = createBaseErrorMsg(specifier);
    const field = isImports ? "imports" : "exports";
    return `${base} using ${field} defined in ${packageUrl}.${reason ? ` ${reason}` : ""}`;
}
class EsmResolveError extends Error {
}
class InvalidModuleSpecifierError extends EsmResolveError {
    constructor(context, isImports, reason) {
        super(createErrorMsg(context, reason, isImports));
    }
}
class InvalidPackageTargetError extends EsmResolveError {
    constructor(context, reason) {
        super(createErrorMsg(context, reason));
    }
}
class NoMatchingConditionsError extends InvalidPackageTargetError {
    constructor(context) {
        super(context, `No conditions matched`);
    }
}
function isUrl(str) {
    try {
        return !!new URL(str);
    }
    catch (_) {
        return false;
    }
}

/** Implementation of PACKAGE_TARGET_RESOLVE https://github.com/nodejs/node/blob/main/doc/api/esm.md */
async function resolvePackageTarget(context, { target, patternMatch, isImports }) {
    const { packageUrl } = context;
    const packageUrlWithTrailingSlash = packageUrl.endsWith("/") ? packageUrl : `${packageUrl}/`;
    // 1. If target is a String, then
    if (typeof target === "string") {
        // 1.i If target does not start with "./", then
        if (!target.startsWith("./")) {
            // 1.i.a If isImports is false, or if target starts with "../" or "/", or if target is a valid URL, then
            if (!isImports || target.startsWith("../") || target.startsWith("/") || isUrl(target)) {
                // 1.i.a.a Throw an Invalid Package Target error.
                throw new InvalidPackageTargetError(context, `Invalid mapping: "${target}".`);
            }
            // 1.i.b If patternMatch is a String, then
            if (typeof patternMatch === "string") {
                // 1.i.b.a Return PACKAGE_RESOLVE(target with every instance of "*" replaced by patternMatch, packageURL + "/")
                return await context.resolveId(target.replace(/\*/g, patternMatch), packageUrlWithTrailingSlash);
            }
            // 1.i.c Return PACKAGE_RESOLVE(target, packageURL + "/").
            return await context.resolveId(target, packageUrlWithTrailingSlash);
        }
        // 1.ii If target split on "/" or "\"
        checkInvalidSegment(context, target);
        // 1.iii Let resolvedTarget be the URL resolution of the concatenation of packageURL and target.
        const resolvedTarget = resolvePath(packageUrlWithTrailingSlash, target);
        // 1.iv Assert: resolvedTarget is contained in packageURL.
        if (!resolvedTarget.startsWith(packageUrl)) {
            throw new InvalidPackageTargetError(context, `Resolved to ${resolvedTarget} which is outside package ${packageUrl}`);
        }
        // 1.v If patternMatch is null, then
        if (!patternMatch) {
            // Return resolvedTarget.
            return resolvedTarget;
        }
        // 1.vi If patternMatch split on "/" or "\" contains invalid segments
        if (includesInvalidSegments(patternMatch.split(/\/|\\/), context.moduleDirs)) {
            // throw an Invalid Module Specifier error.
            throw new InvalidModuleSpecifierError(context);
        }
        // 1.vii Return the URL resolution of resolvedTarget with every instance of "*" replaced with patternMatch.
        return resolvedTarget.replace(/\*/g, patternMatch);
    }
    // 3. Otherwise, if target is an Array, then
    if (Array.isArray(target)) {
        // 3.i If _target.length is zero, return null.
        if (target.length === 0) {
            return null;
        }
        let lastError = null;
        // 3.ii For each item in target, do
        for (const item of target) {
            // Let resolved be the result of PACKAGE_TARGET_RESOLVE of the item
            // continuing the loop on any Invalid Package Target error.
            try {
                const resolved = await resolvePackageTarget(context, {
                    target: item,
                    patternMatch,
                    isImports,
                });
                // If resolved is undefined, continue the loop.
                // Else Return resolved.
                if (resolved !== undefined) {
                    return resolved;
                }
            }
            catch (error) {
                if (!(error instanceof InvalidPackageTargetError)) {
                    throw error;
                }
                else {
                    lastError = error;
                }
            }
        }
        // Return or throw the last fallback resolution null return or error
        if (lastError) {
            throw lastError;
        }
        return null;
    }
    // 2. Otherwise, if target is a non-null Object, then
    if (target && typeof target === "object") {
        // 2.ii For each property of target
        for (const [key, value] of Object.entries(target)) {
            // 2.ii.a If key equals "default" or conditions contains an entry for the key, then
            if ((key === "default" && !context.ignoreDefaultCondition) ||
                context.conditions.includes(key)) {
                // Let targetValue be the value of the property in target.
                // Let resolved be the result of PACKAGE_TARGET_RESOLVE of the targetValue
                const resolved = await resolvePackageTarget(context, {
                    target: value,
                    patternMatch,
                    isImports,
                });
                // If resolved is equal to undefined, continue the loop.
                // Return resolved.
                if (resolved !== undefined) {
                    return resolved;
                }
            }
        }
        // Return undefined.
        return undefined;
    }
    // Otherwise, if target is null, return null.
    if (target === null) {
        return null;
    }
    // Otherwise throw an Invalid Package Target error.
    throw new InvalidPackageTargetError(context, `Invalid exports field.`);
}
/**
 * Check for invalid path segments
 */
function includesInvalidSegments(pathSegments, moduleDirs) {
    const invalidSegments = ["", ".", "..", ...moduleDirs];
    // contains any "", ".", "..", or "node_modules" segments, including percent encoded variants
    return pathSegments.some((v) => invalidSegments.includes(v) || invalidSegments.includes(decodeURI(v)));
}
function checkInvalidSegment(context, target) {
    const pathSegments = target.split(/\/|\\/);
    // after the first "." segment
    const firstDot = pathSegments.indexOf(".");
    firstDot !== -1 && pathSegments.slice(firstDot);
    if (firstDot !== -1 &&
        firstDot < pathSegments.length - 1 &&
        includesInvalidSegments(pathSegments.slice(firstDot + 1), context.moduleDirs)) {
        throw new InvalidPackageTargetError(context, `Invalid mapping: "${target}".`);
    }
}

/** Implementation of PACKAGE_IMPORTS_EXPORTS_RESOLVE https://github.com/nodejs/node/blob/main/doc/api/esm.md */
async function resolvePackageImportsExports(context, { matchKey, matchObj, isImports }) {
    // If matchKey is a key of matchObj and does not contain "*", then
    if (!matchKey.includes("*") && matchKey in matchObj) {
        // Let target be the value of matchObj[matchKey].
        const target = matchObj[matchKey];
        // Return the result of PACKAGE_TARGET_RESOLVE(packageURL, target, null, isImports, conditions).
        const resolved = await resolvePackageTarget(context, { target, patternMatch: "", isImports });
        return resolved;
    }
    // Let expansionKeys be the list of keys of matchObj containing only a single "*"
    const expansionKeys = Object.keys(matchObj)
        // Assert: ends with "/" or contains only a single "*".
        .filter((k) => k.endsWith("/") || k.includes("*"))
        // sorted by the sorting function PATTERN_KEY_COMPARE which orders in descending order of specificity.
        .sort(nodePatternKeyCompare);
    // For each key expansionKey in expansionKeys, do
    for (const expansionKey of expansionKeys) {
        const indexOfAsterisk = expansionKey.indexOf("*");
        // Let patternBase be the substring of expansionKey up to but excluding the first "*" character.
        const patternBase = indexOfAsterisk === -1 ? expansionKey : expansionKey.substring(0, indexOfAsterisk);
        // If matchKey starts with but is not equal to patternBase, then
        if (matchKey.startsWith(patternBase) && matchKey !== patternBase) {
            // Let patternTrailer be the substring of expansionKey from the index after the first "*" character.
            const patternTrailer = indexOfAsterisk !== -1 ? expansionKey.substring(indexOfAsterisk + 1) : "";
            // If patternTrailer has zero length,
            if (patternTrailer.length === 0 ||
                // or if matchKey ends with patternTrailer and the length of matchKey is greater than or equal to the length of expansionKey, then
                (matchKey.endsWith(patternTrailer) && matchKey.length >= expansionKey.length)) {
                // Let target be the value of matchObj[expansionKey].
                const target = matchObj[expansionKey];
                // Let patternMatch be the substring of matchKey starting at the index of the length of patternBase up to the length
                // of matchKey minus the length of patternTrailer.
                const patternMatch = matchKey.substring(patternBase.length, matchKey.length - patternTrailer.length);
                // Return the result of PACKAGE_TARGET_RESOLVE
                const resolved = await resolvePackageTarget(context, {
                    target,
                    patternMatch,
                    isImports,
                });
                return resolved;
            }
        }
    }
    throw new InvalidModuleSpecifierError(context, isImports);
}
/**
 * Implementation of Node's `PATTERN_KEY_COMPARE` function
 */
function nodePatternKeyCompare(keyA, keyB) {
    // Let baseLengthA be the index of "*" in keyA plus one, if keyA contains "*", or the length of keyA otherwise.
    const baseLengthA = keyA.includes("*") ? keyA.indexOf("*") + 1 : keyA.length;
    // Let baseLengthB be the index of "*" in keyB plus one, if keyB contains "*", or the length of keyB otherwise.
    const baseLengthB = keyB.includes("*") ? keyB.indexOf("*") + 1 : keyB.length;
    // if baseLengthA is greater, return -1, if lower 1
    const rval = baseLengthB - baseLengthA;
    if (rval !== 0)
        return rval;
    // If keyA does not contain "*", return 1.
    if (!keyA.includes("*"))
        return 1;
    // If keyB does not contain "*", return -1.
    if (!keyB.includes("*"))
        return -1;
    // If the length of keyA is greater than the length of keyB, return -1.
    // If the length of keyB is greater than the length of keyA, return 1.
    // Else Return 0.
    return keyB.length - keyA.length;
}

/** Implementation of PACKAGE_EXPORTS_RESOLVE https://github.com/nodejs/node/blob/main/doc/api/esm.md */
async function resolvePackageExports(context, subpath, exports) {
    if (exports === null)
        return undefined;
    if (subpath === ".") {
        let mainExport;
        if (typeof exports === "string" || Array.isArray(exports) || isConditions(exports)) {
            mainExport = exports;
        }
        else if (exports["."]) {
            mainExport = exports["."];
        }
        if (mainExport) {
            if (context.ignoreDefaultCondition && typeof mainExport === "string") {
                return undefined;
            }
            const resolved = await resolvePackageTarget(context, {
                target: mainExport,
                isImports: false,
            });
            // If resolved is not null or undefined, return resolved.
            if (resolved) {
                return resolved;
            }
            else {
                throw new NoMatchingConditionsError(context);
            }
        }
    }
    else if (isMappings(exports)) {
        // Let resolved be the result of PACKAGE_IMPORTS_EXPORTS_RESOLVE
        const resolvedMatch = await resolvePackageImportsExports(context, {
            matchKey: subpath,
            matchObj: exports,
            isImports: false,
        });
        // If resolved is not null or undefined, return resolved.
        if (resolvedMatch) {
            return resolvedMatch;
        }
    }
    // 4. Throw a Package Path Not Exported error.
    throw new InvalidModuleSpecifierError(context);
}
/** Conditions is an export object where all keys are conditions(not a path starting with .). E.g. import, default, types, etc. */
function isConditions(item) {
    return typeof item === "object" && Object.keys(item).every((k) => !k.startsWith("."));
}
/**
 * Mappings is an export object where all keys start with '.
 */
function isMappings(exports) {
    return typeof exports === "object" && !isConditions(exports);
}

// returns the imported package name for bare module imports
function parseNodeModuleSpecifier(id) {
    if (id.startsWith(".") || id.startsWith("/")) {
        return null;
    }
    const split = id.split("/");
    // @my-scope/my-package/foo.js -> @my-scope/my-package
    // @my-scope/my-package -> @my-scope/my-package
    if (split[0][0] === "@") {
        return { packageName: `${split[0]}/${split[1]}`, subPath: split.slice(2).join("/") };
    }
    // my-package/foo.js -> my-package
    // my-package -> my-package
    return { packageName: split[0], subPath: split.slice(1).join("/") };
}

class ResolveModuleError extends Error {
    code;
    constructor(code, message) {
        super(message);
        this.code = code;
    }
}
const defaultDirectoryIndexFiles = ["index.mjs", "index.js"];
/**
 * Resolve a module
 * @param host
 * @param specifier
 * @param options
 * @returns
 * @throws {ResolveModuleError} When the module cannot be resolved.
 */
async function resolveModule(host, specifier, options) {
    const realpath = async (x) => normalizePath(await host.realpath(x));
    const { baseDir } = options;
    const absoluteStart = await realpath(resolvePath(baseDir));
    if (!(await isDirectory(host, absoluteStart))) {
        throw new TypeError(`Provided basedir '${baseDir}'is not a directory.`);
    }
    // Check if the module name is referencing a path(./foo, /foo, file:/foo)
    if (/^(?:\.\.?(?:\/|$)|\/|([A-Za-z]:)?[/\\])/.test(specifier)) {
        const res = resolvePath(absoluteStart, specifier);
        const m = (await loadAsFile(res)) || (await loadAsDirectory(res));
        if (m) {
            return m;
        }
    }
    // Try to resolve as a node_module package.
    const module = await resolveAsNodeModule(specifier, absoluteStart);
    if (module)
        return module;
    throw new ResolveModuleError("MODULE_NOT_FOUND", `Cannot find module '${specifier}' from '${baseDir}'`);
    /**
     * Returns a list of all the parent directory and the given one.
     */
    function listDirHierarchy(baseDir) {
        const paths = [baseDir];
        let current = getDirectoryPath(baseDir);
        while (current !== paths[paths.length - 1]) {
            paths.push(current);
            current = getDirectoryPath(current);
        }
        return paths;
    }
    /**
     * Try to import a package with that name in the current directory.
     */
    async function resolveSelf({ packageName, subPath }, dir) {
        const pkgFile = resolvePath(dir, "package.json");
        if (!(await isFile(host, pkgFile)))
            return undefined;
        const pkg = await readPackage(host, pkgFile);
        // Node Spec says that you shouldn't lookup past the first package.json. However we used to support that so keeping this.
        if (pkg.name !== packageName)
            return undefined;
        return loadPackage(dir, pkg, subPath);
    }
    /**
     * Equivalent implementation to node LOAD_NODE_MODULES with a few non supported features.
     * Cannot load any random file under the load path(only packages).
     */
    async function resolveAsNodeModule(importSpecifier, baseDir) {
        const module = parseNodeModuleSpecifier(importSpecifier);
        if (module === null)
            return undefined;
        const dirs = listDirHierarchy(baseDir);
        for (const dir of dirs) {
            const self = await resolveSelf(module, dir);
            if (self)
                return self;
            const n = await loadPackageAtPath(joinPaths(dir, "node_modules", module.packageName), module.subPath);
            if (n)
                return n;
        }
        return undefined;
    }
    async function loadPackageAtPath(path, subPath) {
        const pkgFile = resolvePath(path, "package.json");
        if (!(await isFile(host, pkgFile)))
            return undefined;
        const pkg = await readPackage(host, pkgFile);
        const n = await loadPackage(path, pkg, subPath);
        if (n)
            return n;
        return undefined;
    }
    /**
     * Try to load using package.json exports.
     * @param importSpecifier A combination of the package name and exports entry.
     * @param directory `node_modules` directory.
     */
    async function resolveNodePackageExports(subPath, pkg, pkgDir) {
        if (!pkg.exports)
            return undefined;
        let match;
        try {
            match = await resolvePackageExports({
                packageUrl: pathToFileURL(pkgDir),
                specifier: specifier,
                moduleDirs: ["node_modules"],
                conditions: options.conditions ?? [],
                ignoreDefaultCondition: options.fallbackOnMissingCondition,
                resolveId: (id, baseDir) => {
                    throw new ResolveModuleError("INVALID_MODULE", "Not supported");
                },
            }, subPath === "" ? "." : `./${subPath}`, pkg.exports);
        }
        catch (error) {
            if (error instanceof NoMatchingConditionsError) {
                // For back compat we allow to fallback to main field for the `.` entry.
                if (subPath === "") {
                    return;
                }
                else {
                    throw new ResolveModuleError("INVALID_MODULE", error.message);
                }
            }
            else if (error instanceof InvalidPackageTargetError) {
                throw new ResolveModuleError("INVALID_MODULE_EXPORT_TARGET", error.message);
            }
            else if (error instanceof EsmResolveError) {
                throw new ResolveModuleError("INVALID_MODULE", error.message);
            }
            else {
                throw error;
            }
        }
        if (!match)
            return undefined;
        const resolved = await resolveEsmMatch(match);
        return {
            type: "module",
            mainFile: resolved,
            manifest: pkg,
            path: pkgDir,
        };
    }
    async function resolveEsmMatch(match) {
        const resolved = await realpath(fileURLToPath(match));
        if (await isFile(host, resolved)) {
            return resolved;
        }
        throw new ResolveModuleError("INVALID_MODULE_EXPORT_TARGET", `Import "${specifier}" resolving to "${resolved}" is not a file.`);
    }
    async function loadAsDirectory(directory) {
        const pkg = await loadPackageAtPath(directory);
        if (pkg) {
            return pkg;
        }
        for (const file of options.directoryIndexFiles ?? defaultDirectoryIndexFiles) {
            const resolvedFile = await loadAsFile(joinPaths(directory, file));
            if (resolvedFile) {
                return resolvedFile;
            }
        }
        return undefined;
    }
    async function loadPackage(directory, pkg, subPath) {
        const e = await resolveNodePackageExports(subPath ?? "", pkg, directory);
        if (e)
            return e;
        if (subPath !== undefined && subPath !== "") {
            return undefined;
        }
        return loadPackageLegacy(directory, pkg);
    }
    async function loadPackageLegacy(directory, pkg) {
        const mainFile = options.resolveMain ? options.resolveMain(pkg) : pkg.main;
        if (typeof mainFile !== "string") {
            throw new TypeError(`package "${pkg.name}" main must be a string but was '${mainFile}'`);
        }
        const mainFullPath = resolvePath(directory, mainFile);
        let loaded;
        try {
            loaded = (await loadAsFile(mainFullPath)) ?? (await loadAsDirectory(mainFullPath));
        }
        catch (e) {
            throw new Error(`Cannot find module '${mainFullPath}'. Please verify that the package.json has a valid "main" entry`);
        }
        if (loaded) {
            if (loaded.type === "module") {
                return loaded;
            }
            return {
                type: "module",
                path: await realpath(directory),
                mainFile: loaded.path,
                manifest: pkg,
            };
        }
        else {
            throw new ResolveModuleError("INVALID_MAIN", `Package ${pkg.name} main file "${mainFile}" is not pointing to a valid file or directory.`);
        }
    }
    async function loadAsFile(file) {
        if (await isFile(host, file)) {
            return resolvedFile(file);
        }
        const extensions = [".mjs", ".js"];
        for (const ext of extensions) {
            const fileWithExtension = file + ext;
            if (await isFile(host, fileWithExtension)) {
                return resolvedFile(fileWithExtension);
            }
        }
        return undefined;
    }
    async function resolvedFile(path) {
        return { type: "file", path: await realpath(path) };
    }
}
async function readPackage(host, pkgfile) {
    const content = await host.readFile(pkgfile);
    return JSON.parse(content);
}
async function isDirectory(host, path) {
    try {
        const stats = await host.stat(path);
        return stats.isDirectory();
    }
    catch (e) {
        if (e.code === "ENOENT" || e.code === "ENOTDIR") {
            return false;
        }
        throw e;
    }
}
async function isFile(host, path) {
    try {
        const stats = await host.stat(path);
        return stats.isFile();
    }
    catch (e) {
        if (e.code === "ENOENT" || e.code === "ENOTDIR") {
            return false;
        }
        throw e;
    }
}
function pathToFileURL(path) {
    return `file://${path}`;
}
function fileURLToPath(url) {
    if (!url.startsWith("file://"))
        throw new Error("Cannot convert non file: URL to path");
    const pathname = url.slice("file://".length);
    for (let n = 0; n < pathname.length; n++) {
        if (pathname[n] === "%") {
            const third = pathname.codePointAt(n + 2) | 0x20;
            if (pathname[n + 1] === "2" && third === 102) {
                throw new Error("Invalid url to path: must not include encoded / characters");
            }
        }
    }
    return decodeURIComponent(pathname);
}

export { ResolveModuleError, resolveModule };
