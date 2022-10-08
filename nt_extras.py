import bpy
import itertools

DATA_TYPE = ["FLOAT", "INT", "FLOAT_VECTOR", "FLOAT_COLOR", "BOOLEAN"]
DOMAIN = ["POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE"]

math = [
    [" M ADD", "Add (A) MATH"],
    [" M SUBTRACT", "Subtract (S) MATH"],
    [" M MULTIPLY", "Multiply (M) MATH"],
    [" M DIVIDE", "Divide (D) MATH"],
    [" M MULTIPLY_ADD", "Multiply Add (MA) MATH"],
    [" M POWER", "Power (P) MATH"],
    [" M LOGARITHM", "Logarithm (L) MATH"],
    [" M SQRT", "Square Root (SQ) MATH"],
    [" M INVERSE_SQRT", "Inverse Square Root (ISQ) MATH"],
    [" M ABSOLUTE", "Absolute (A) MATH"],
    [" M EXPONENT", "Exponent (E) MATH"],
    [" M MINIMUM", "Minimum (M) MATH"],
    [" M MAXIMUM", "Maximum (M) MATH"],
    [" M LESS_THAN", "Less Than (LT) MATH"],
    [" M GREATER_THAN", "Greater Than (GT) MATH"],
    [" M SIGN", "Sign (S) MATH"],
    [" M COMPARE", "Compare (C) MATH"],
    [" M SMOOTH_MIN", "Smooth Minimum (SM) MATH"],
    [" M SMOOTH_MAX", "Smooth Maximum (SM) MATH"],
    [" M ROUND", "Round (R) MATH"],
    [" M FLOOR", "Floor (F) MATH"],
    [" M CEIL", "Ceiling (C) MATH"],
    [" M TRUNC", "Truncate (T) MATH"],
    [" M FRACT", "Fraction (F) MATH"],
    [" M MODULO", "Modulo (M) MATH"],
    [" M WRAP", "Wrap (W) MATH"],
    [" M SNAP", "Snap (S) MATH"],
    [" M PINGPONG", "Ping-Pong (PP) MATH"],
    [" M SINE", "Sine (S) MATH"],
    [" M COSINE", "Cosine (C) MATH"],
    [" M TANGENT", "Tangent (T) MATH"],
    [" M ARCSINE", "ArcSine (AS) MATH"],
    [" M ARCCOSINE", "Arccosine (AC) MATH"],
    [" M ARCTANGENT", "Arctangent (AT) MATH"],
    [" M ARCTAN2", "Arctan2 (AT) MATH"],
    [" M SINH", "Hyperbolic Sine (HS) MATH"],
    [" M COSH", "Hyperbolic Cosine (HC) MATH"],
    [" M TANH", "Hyperbolic Tangent (HT) MATH"],
    [" M RADIANS", "To Radians (TR) MATH"],
    [" M DEGREES", "To Degrees (TD) MATH"],
]

vector_math = [
    [" VM ADD", "Add (A) VEC MATH"],
    [" VM SUBTRACT", "Subtract (S) VEC MATH"],
    [" VM MULTIPLY", "Multiply (M) VEC MATH"],
    [" VM DIVIDE", "Divide (D) VEC MATH"],
    [" VM CROSS_PRODUCT", "Cross Product (CP) VEC MATH"],
    [" VM PROJECT", "Project (P) VEC MATH"],
    [" VM REFRACT", "Refract (R) VEC MATH"],
    [" VM REFLECT", "Reflect (R) VEC MATH"],
    [" VM DOT_PRODUCT", "Dot Product (DP) VEC MATH"],
    [" VM DISTANCE", "Distance (D) VEC MATH"],
    [" VM MULTIPLY_ADD", "Multiply Add (MA) VEC MATH"],
    [" VM FACEFORWARD", "Faceforward (F) VEC MATH"],
    [" VM LENGTH", "Length (L) VEC MATH"],
    [" VM SCALE", "Scale (S) VEC MATH"],
    [" VM NORMALIZE", "Normalize (N) VEC MATH"],
    [" VM ABSOLUTE", "Absolute (A) VEC MATH"],
    [" VM MINIMUM", "Minimum (M) VEC MATH"],
    [" VM MAXIMUM", "Maximum (M) VEC MATH"],
    [" VM FLOOR", "Floor (F) VEC MATH"],
    [" VM CEIL", "Ceiling (C) VEC MATH"],
    [" VM FRACTION", "Fraction (F) VEC MATH"],
    [" VM MODULO", "Modulo (M) VEC MATH"],
    [" VM WRAP", "Wrap (W) VEC MATH"],
    [" VM SNAP", "Snap (S) VEC MATH"],
    [" VM SINE", "Sine (S) VEC MATH"],
    [" VM COSINE", "Cosine (C) VEC MATH"],
    [" VM TANGENT", "Tangent (T) VEC MATH"],
]

color = [
    [" C VALUE", "Value (V) COLOR"],
    [" C COLOR", "Color (C) COLOR"],
    [" C SATURATION", "Saturation (S) COLOR"],
    [" C HUE", "Hue (H) COLOR"],
    [" C DIVIDE", "Divide (D) COLOR"],
    [" C SUBTRACT", "Subtract (S) COLOR"],
    [" C DIFFERENCE", "Difference (D) COLOR"],
    [" C LINEAR_LIGHT", "Linear Light (LL) COLOR"],
    [" C SOFT_LIGHT", "Soft Light (SL) COLOR"],
    [" C OVERLAY", "Overlay (O) COLOR"],
    [" C ADD", "Add (A) COLOR"],
    [" C DODGE", "Dodge (D) COLOR"],
    [" C SCREEN", "Screen (S) COLOR"],
    [" C LIGHTEN", "Lighten (L) COLOR"],
    [" C BURN", "Burn (B) COLOR"],
    [" C MULTIPLY", "Multiply (M) COLOR"],
    [" C DARKEN", "Darken (D) COLOR"],
    [" C MIX", "Mix (M) COLOR"],
]

boolean_math = [
    [" BM AND", "And (A) BOOL MATH"],
    [" BM OR", "Or (O) BOOL MATH"],
    [" BM NOT", "Not (N) BOOL MATH"],
    [" BM NAND", "Not And (NA) BOOL MATH"],
    [" BM NOR", "Nor (N) BOOL MATH"],
    [" BM XNOR", "Equal (E) BOOL MATH"],
    [" BM XOR", "Not Equal (NE) BOOL MATH"],
    [" BM IMPLY", "Imply (I) BOOL MATH"],
    [" BM NIMPLY", "Subtract (S) BOOL MATH"],
]

random_value = [
    [" RV FLOAT", "Float (F) RAND VAL"],
    [" RV INT", "Integer (I) RAND VAL"],
    [" RV FLOAT_VECTOR", "Vector (V) RAND VAL"],
    [" RV BOOLEAN", "Boolean (B) RAND VAL"],
]

switch = [
    [" SW FLOAT", "Float (F) SWITCH"],
    [" SW INT", "Integer (I) SWITCH"],
    [" SW BOOLEAN", "Boolean (B) SWITCH"],
    [" SW VECTOR", "Vector (V) SWITCH"],
    [" SW STRING", "String (S) SWITCH"],
    [" SW RGBA", "Color (C) SWITCH"],
    [" SW OBJECT", "Object (O) SWITCH"],
    [" SW IMAGE", "Image (I) SWITCH"],
    [" SW GEOMETRY", "Geometry (G) SWITCH"],
    [" SW COLLECTION", "Collection (C) SWITCH"],
    [" SW TEXTURE", "Texture (T) SWITCH"],
    [" SW MATERIAL", "Material (M) SWITCH"],
]

sep_col = [
    [" SEP RGB", "RGB (SR) SEP RGB"],
    [" SEP HSV", "HSV (SH) SEP HSV"],
    [" SEP HSL", "HSL (SL) SEP HSL"]
]

capture_attr = [
    [" CAP {} {}".format(d[0], d[1]),
     "{} {} ({}{}) CAP ATTR".format(str.capitalize(d[0].replace("FLOAT_", "")), str.capitalize(d[1]), d[0][0], d[1][0])]
    for d in itertools.product(DATA_TYPE, DOMAIN)]
