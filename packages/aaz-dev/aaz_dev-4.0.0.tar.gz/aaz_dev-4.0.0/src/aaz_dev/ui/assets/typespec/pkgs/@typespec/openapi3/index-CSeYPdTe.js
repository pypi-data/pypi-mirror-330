import { createTypeSpecLibrary, paramMessage, $encodedName, getEncode } from '@typespec/compiler';

/** TypeSpec Xml Library Definition */
const $lib = createTypeSpecLibrary({
    name: "@typespec/xml",
    diagnostics: {
        "ns-enum-not-declaration": {
            severity: "error",
            messages: {
                default: "Enum member used as namespace must be part of an enum marked with @nsDeclaration.",
            },
        },
        "invalid-ns-declaration-member": {
            severity: "error",
            messages: {
                default: paramMessage `Enum member ${"name"} must have a value that is the XML namespace url.`,
            },
        },
        "ns-missing-prefix": {
            severity: "error",
            messages: {
                default: "When using a string namespace you must provide a prefix as the 2nd argument.",
            },
        },
        "prefix-not-allowed": {
            severity: "error",
            messages: {
                default: "@ns decorator cannot have the prefix parameter set when using an enum member.",
            },
        },
        "ns-not-uri": {
            severity: "error",
            messages: {
                default: `Namespace ${"namespace"} is not a valid URI.`,
            },
        },
    },
    state: {
        attribute: { description: "Mark a model property to be serialized as xml attribute" },
        unwrapped: {
            description: "Mark a model property to be serialized without a node wrapping the content.",
        },
        ns: { description: "Namespace data" },
        nsDeclaration: { description: "Mark an enum that declares Xml Namespaces" },
    },
});
const { reportDiagnostic, createStateSymbol, stateKeys: XmlStateKeys } = $lib;

/** {@inheritDoc NameDecorator}  */
const $name = (context, target, name) => {
    context.call($encodedName, target, "application/xml", name);
};
/** {@inheritDoc AttributeDecorator} */
const $attribute = (context, target) => {
    context.program.stateSet(XmlStateKeys.attribute).add(target);
};
/**
 * Check if the given property should be serialized as an attribute instead of a node.
 */
function isAttribute(program, target) {
    return program.stateSet(XmlStateKeys.attribute).has(target);
}
/** {@inheritdoc UnwrappedDecorator} */
const $unwrapped = (context, target) => {
    context.program.stateSet(XmlStateKeys.unwrapped).add(target);
};
/**
 * Check if the given property should be unwrapped in the XML containing node.
 */
function isUnwrapped(program, target) {
    return program.stateSet(XmlStateKeys.unwrapped).has(target);
}
/** {@inheritdoc NsDeclarationsDecorator} */
const $nsDeclarations = (context, target) => {
    context.program.stateSet(XmlStateKeys.nsDeclaration).add(target);
};
function isNsDeclarationsEnum(program, target) {
    return program.stateSet(XmlStateKeys.nsDeclaration).has(target);
}
/** {@inheritdoc NsDecorator} */
const $ns = (context, target, namespace, prefix) => {
    const data = getData(context, namespace, prefix);
    if (data) {
        if (validateNamespaceIsUri(context, data.namespace)) {
            context.program.stateMap(XmlStateKeys.nsDeclaration).set(target, data);
        }
    }
};
/**
 * Get the namespace and prefix for the given type.
 */
function getNs(program, target) {
    return program.stateMap(XmlStateKeys.nsDeclaration).get(target);
}
function getData(context, namespace, prefix) {
    switch (namespace.kind) {
        case "String":
            if (!prefix) {
                reportDiagnostic(context.program, {
                    code: "ns-missing-prefix",
                    target: context.decoratorTarget,
                });
                return undefined;
            }
            return { namespace: namespace.value, prefix };
        case "EnumMember":
            if (!isNsDeclarationsEnum(context.program, namespace.enum)) {
                reportDiagnostic(context.program, {
                    code: "ns-enum-not-declaration",
                    target: context.decoratorTarget,
                });
                return undefined;
            }
            if (prefix !== undefined) {
                reportDiagnostic(context.program, {
                    code: "prefix-not-allowed",
                    target: context.getArgumentTarget(1),
                    format: { name: namespace.name },
                });
            }
            if (typeof namespace.value !== "string") {
                reportDiagnostic(context.program, {
                    code: "invalid-ns-declaration-member",
                    target: context.decoratorTarget,
                    format: { name: namespace.name },
                });
                return undefined;
            }
            return { namespace: namespace.value, prefix: namespace.name };
        default:
            return undefined;
    }
}
function validateNamespaceIsUri(context, namespace) {
    try {
        new URL(namespace);
        return true;
    }
    catch {
        reportDiagnostic(context.program, {
            code: "ns-not-uri",
            target: context.getArgumentTarget(0),
            format: { namespace },
        });
        return false;
    }
}

/**
 * Resolve how the given type should be encoded in XML.
 * This will return the default encoding for each types.(e.g. TypeSpec.Xml.Encoding.xmlDateTime for a utcDatetime)
 * @param program
 * @param type
 * @returns
 */
function getXmlEncoding(program, type) {
    const encodeData = getEncode(program, type);
    if (encodeData) {
        return encodeData;
    }
    const def = getDefaultEncoding(type.kind === "Scalar" ? type : type.type);
    if (def === undefined) {
        return undefined;
    }
    return { encoding: def, type: program.checker.getStdType("string") };
}
function getDefaultEncoding(type) {
    switch (type.name) {
        case "utcDateTime":
        case "offsetDateTime":
            return "TypeSpec.Xml.Encoding.xmlDateTime";
        case "plainDate":
            return "TypeSpec.Xml.Encoding.xmlDate";
        case "plainTime":
            return "TypeSpec.Xml.Encoding.xmlTime";
        case "duration":
            return "TypeSpec.Xml.Encoding.xmlDuration";
        case "bytes":
            return "TypeSpec.Xml.Encoding.xmlBase64Binary";
        default:
            return undefined;
    }
}

/** @internal */
const $decorators = {
    "TypeSpec.Xml": {
        attribute: $attribute,
        name: $name,
        ns: $ns,
        nsDeclarations: $nsDeclarations,
        unwrapped: $unwrapped,
    },
};

export { $attribute, $decorators, $lib, $name, $ns, $nsDeclarations, $unwrapped, getNs, getXmlEncoding, isAttribute, isUnwrapped };
