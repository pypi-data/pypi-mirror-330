/* ------------------------------------------------------------------------

   unicodedata -- Provides access to the Unicode database.

   Data was extracted from the UnicodeData.txt file.
   The current version number is reported in the unidata_version constant.

   Written by Marc-Andre Lemburg (mal@lemburg.com).
   Modified for Python 2.0 by Fredrik Lundh (fredrik@pythonware.com)
   Modified by Martin v. Löwis (martin@v.loewis.de)

   Copyright (c) Corporation for National Research Initiatives.

   ------------------------------------------------------------------------ */

#if PY_MINOR_VERSION < 13
#define PY_SSIZE_T_CLEAN
#endif

// a slightly goofy hack to make the argument clinic work right
#define Py_LIMITED_API
#undef Py_LIMITED_API
#include "Python.h"
#include "pycore_ucnhash.h"       // _PyUnicode_Name_CAPI
#include "unicodectype.h"

#include <stdbool.h>
#include <stddef.h>               // offsetof()

#if PY_MINOR_VERSION < 12
#include "structmember.h"
#define Py_READONLY    READONLY
#define Py_T_STRING    T_STRING
#define Py_T_OBJECT_EX T_OBJECT_EX
#endif

#if PY_MINOR_VERSION < 11
#define _Py_CAST(type, expr) ((type)(expr))
#define _PyCFunction_CAST(func) \
    _Py_CAST(PyCFunction, _Py_CAST(void(*)(void), (func)))
#endif

#if PY_MINOR_VERSION < 10
static PyObject *
Py_NewRef(PyObject *o)
{
    Py_INCREF(o);
    return o;
}
#endif

/*[clinic input]
module unicodedata
class unicodedata.UCD 'PreviousDBVersion *' '<not used>'
[clinic start generated code]*/
/*[clinic end generated code: output=da39a3ee5e6b4b0d input=e47113e05924be43]*/

/* character properties */

typedef struct {
    const unsigned char category;       /* index into
                                           _PyUnicodePlus_CategoryNames */
    const unsigned char combining;      /* combining class value 0 - 255 */
    const unsigned char bidirectional;  /* index into
                                           _PyUnicodePlus_BidirectionalNames */
    const unsigned char mirrored;       /* true if mirrored in bidir mode */
    const unsigned char east_asian_width;       /* index into
                                                   _PyUnicodePlus_EastAsianWidth */
    const unsigned char normalization_quick_check; /* see is_normalized() */
} _PyUnicodePlus_DatabaseRecord;

typedef struct {
    const int script;         /* index into
                                           _PyUnicodePlus_Script */
    const int block;          /* index into
                                           _PyUnicodePlus_Block */
    const int script_extensions; /* index into
                                           _PyUnicodePlus_Script_Extensions */
    const int indic_conjunct_break; /* index into
                                           _PyUnicodePlus_Indic_Conjunct_Break */
    const int indic_positional_category; /* index into
                                           _PyUnicodePlus_Indic_Positional_Category */
    const int indic_syllabic_category;   /* index into
                                           _PyUnicodePlus_Indic_Syllabic_Category */
    const int grapheme_cluster_break;   /* index into
                                           _PyUnicodePlus_Grapheme_Cluster_Break */
    const int word_break;   /* index into
                                           _PyUnicodePlus_Word_Break */
    const int sentence_break;   /* index into
                                           _PyUnicodePlus_Sentence_Break */
    const int line_break;   /* index into
                                           _PyUnicodePlus_Line_Break */
    const int vertical_orientation;   /* index into
                                           _PyUnicodePlus_Vertical_Orientation */
    const int age;            /* index into
                                           _PyUnicodePlus_Age */
} _PyUnicodePlus_PropertySet;

typedef struct {
    const unsigned char total_strokes_g;  /* index into _PyUnicodePlus_TotalStrokes_G */
    const unsigned char total_strokes_t;  /* index into _PyUnicodePlus_TotalStrokes_T */
} _PyUnicodePlus_UnihanSet;

typedef struct change_record {
    /* sequence of fields should be the same as in merge_old_version */
    const unsigned char bidir_changed;
    const unsigned char category_changed;
    const unsigned char decimal_changed;
    const unsigned char mirrored_changed;
    const unsigned char east_asian_width_changed;
    const double numeric_changed;
    const unsigned char script_changed;
    const unsigned char block_changed;
    const unsigned char script_extensions_changed;
    const unsigned char indic_conjunct_break_changed;
    const unsigned char indic_positional_category_changed;
    const unsigned char indic_syllabic_category_changed;
    const unsigned char grapheme_cluster_break_changed;
    const unsigned char word_break_changed;
    const unsigned char sentence_break_changed;
    const unsigned char line_break_changed;
    const unsigned char vertical_orientation_changed;
    const unsigned char age_changed;
    const unsigned char total_strokes_g_changed;
    const unsigned char total_strokes_t_changed;
} change_record;

/* data file generated by makeunicodedata.py */
#include "unicodedata_db.h"

static const _PyUnicodePlus_DatabaseRecord*
_getrecord_ex(Py_UCS4 code)
{
    int index;
    if (code >= 0x110000)
        index = 0;
    else {
        index = index1[(code>>SHIFT)];
        index = index2[(index<<SHIFT)+(code&((1<<SHIFT)-1))];
    }

    return &_PyUnicodePlus_Database_Records[index];
}

/* property set data file generated by makeunicodedata.py */
#include "unicodeprop_db.h"

static const _PyUnicodePlus_PropertySet*
_getpropset_ex(Py_UCS4 code)
{
    int index;
    if (code >= 0x110000)
        index = 0;
    else {
        index = prop_index1[(code>>PROP_SHIFT)];
        index = prop_index2[(index<<PROP_SHIFT)+(code&((1<<PROP_SHIFT)-1))];
    }

    return &_PyUnicodePlus_Property_Sets[index];
}

#include "unicodeunihan_db.h"

static const _PyUnicodePlus_UnihanSet*
_getunihanset_ex(Py_UCS4 code)
{
    int index;
    if (code >= 0x110000)
        index = 0;
    else {
        index = unihan_index1[(code>>UNIHAN_SHIFT)];
        index = unihan_index2[(index<<UNIHAN_SHIFT)+(code&((1<<UNIHAN_SHIFT)-1))];
    }

    return &_PyUnicodePlus_Unihan_Sets[index];
}
/* ------------- Previous-version API ------------------------------------- */
typedef struct previous_version {
    PyObject_HEAD
    const char *name;
    const PyObject *property_value_aliases;
    const PyObject *property_value_by_alias;
    const change_record* (*getrecord)(Py_UCS4);
    Py_UCS4 (*normalization)(Py_UCS4);
} PreviousDBVersion;

#define PreviousDBVersion_CAST(op)  ((PreviousDBVersion *)(op))

#if PY_MINOR_VERSION < 13
    #include "unicodedata.3.12.c.h"
#else
    #include "unicodedata.c.h"
#endif

#define get_old_record(self, v)    (PreviousDBVersion_CAST(self)->getrecord(v))

static PyMemberDef DB_members[] = {
        {"unidata_version", Py_T_STRING, offsetof(PreviousDBVersion, name), Py_READONLY},
        {"property_value_aliases", Py_T_OBJECT_EX, offsetof(PreviousDBVersion, property_value_aliases), Py_READONLY},
        {"property_value_by_alias", Py_T_OBJECT_EX, offsetof(PreviousDBVersion, property_value_by_alias), Py_READONLY},
        {NULL}
};

// Check if self is an unicodedata.UCD instance.
// If self is NULL (when the PyCapsule C API is used), return 0.
// PyModule_Check() is used to avoid having to retrieve the ucd_type.
// See unicodedata_functions comment to the rationale of this macro.
#define UCD_Check(self) (self != NULL && !PyModule_Check(self))

#if PY_MINOR_VERSION < 10
static PyTypeObject UCD_Type;
static PyObject*
new_previous_version(const char*name, const change_record* (*getrecord)(Py_UCS4),
                     Py_UCS4 (*normalization)(Py_UCS4),
                     const PyObject *property_value_aliases,
                     const PyObject *property_value_by_alias)
{
        PreviousDBVersion *self;
        self = PyObject_New(PreviousDBVersion, &UCD_Type);
        if (self == NULL)
                return NULL;
        self->name = name;
        self->getrecord = getrecord;
        self->normalization = normalization;
        self->property_value_aliases = property_value_aliases;
        self->property_value_by_alias = property_value_by_alias;
        return (PyObject*)self;
}
#else
static PyObject*
new_previous_version(PyTypeObject *ucd_type,
                     const char*name, const change_record* (*getrecord)(Py_UCS4),
                     Py_UCS4 (*normalization)(Py_UCS4),
                     const PyObject *property_value_aliases,
                     const PyObject *property_value_by_alias)
{
    PreviousDBVersion *self;
    self = PyObject_GC_New(PreviousDBVersion, ucd_type);
    if (self == NULL)
        return NULL;
    self->name = name;
    self->getrecord = getrecord;
    self->normalization = normalization;
    self->property_value_aliases = property_value_aliases;
    self->property_value_by_alias = property_value_by_alias;
    PyObject_GC_Track(self);
    return (PyObject*)self;
}
#endif

#ifdef PYPY_VERSION
#include "pypy_ctype.h"
#endif

/* --- Module API --------------------------------------------------------- */

/*[clinic input]
unicodedata.UCD.decimal

    self: self
    chr: int(accept={str})
    default: object=NULL
    /

Converts a Unicode character into its equivalent decimal value.

Returns the decimal value assigned to the character chr as integer.
If no such value is defined, default is returned, or, if not given,
ValueError is raised.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_decimal_impl(PyObject *self, int chr,
                             PyObject *default_value)
/*[clinic end generated code: output=be23376e1a185231 input=933f8107993f23d0]*/
{
    int have_old = 0;
    long rc;
    Py_UCS4 c = (Py_UCS4)chr;

    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0) {
            /* unassigned */
            have_old = 1;
            rc = -1;
        }
        else if (old->decimal_changed != 0xFF) {
            have_old = 1;
            rc = old->decimal_changed;
        }
    }

    if (!have_old)
        rc = _PyUnicodePlus_ToDecimalDigit(c);
    if (rc < 0) {
        if (default_value == NULL) {
            PyErr_SetString(PyExc_ValueError,
                            "not a decimal");
            return NULL;
        }
        else {
            return Py_NewRef(default_value);
        }
    }
    return PyLong_FromLong(rc);
}

/*[clinic input]
unicodedata.UCD.digit

    self: self
    chr: int(accept={str})
    default: object=NULL
    /

Converts a Unicode character into its equivalent digit value.

Returns the digit value assigned to the character chr as integer.
If no such value is defined, default is returned, or, if not given,
ValueError is raised.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_digit_impl(PyObject *self, int chr, PyObject *default_value)
/*[clinic end generated code: output=96e18c950171fd2f input=e27d6e4565cd29f2]*/
{
    long rc;
    Py_UCS4 c = (Py_UCS4)chr;
    rc = _PyUnicodePlus_ToDigit(c);
    if (rc < 0) {
        if (default_value == NULL) {
            PyErr_SetString(PyExc_ValueError, "not a digit");
            return NULL;
        }
        else {
            return Py_NewRef(default_value);
        }
    }
    return PyLong_FromLong(rc);
}

/*[clinic input]
unicodedata.UCD.numeric

    self: self
    chr: int(accept={str})
    default: object=NULL
    /

Converts a Unicode character into its equivalent numeric value.

Returns the numeric value assigned to the character chr as float.
If no such value is defined, default is returned, or, if not given,
ValueError is raised.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_numeric_impl(PyObject *self, int chr,
                             PyObject *default_value)
/*[clinic end generated code: output=53ce281fe85b10c4 input=fdf5871a5542893c]*/
{
    int have_old = 0;
    double rc;
    Py_UCS4 c = (Py_UCS4)chr;

    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0) {
            /* unassigned */
            have_old = 1;
            rc = -1.0;
        }
        else if (old->decimal_changed != 0xFF) {
            have_old = 1;
            rc = old->decimal_changed;
        }
    }

    if (!have_old)
        rc = _PyUnicodePlus_ToNumeric(c);
    if (rc == -1.0) {
        if (default_value == NULL) {
            PyErr_SetString(PyExc_ValueError, "not a numeric character");
            return NULL;
        }
        else {
            return Py_NewRef(default_value);
        }
    }
    return PyFloat_FromDouble(rc);
}

/*[clinic input]
unicodedata.UCD.category

    self: self
    chr: int(accept={str})
    /

Returns the general category assigned to the character chr as string.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_category_impl(PyObject *self, int chr)
/*[clinic end generated code: output=8571539ee2e6783a input=27d6f3d85050bc06]*/
{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getrecord_ex(c)->category;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed != 0xFF)
            index = old->category_changed;
    }
    return PyUnicode_FromString(_PyUnicodePlus_CategoryNames[index]);
}

/*[clinic input]
unicodedata.UCD.bidirectional

    self: self
    chr: int(accept={str})
    /

Returns the bidirectional class assigned to the character chr as string.

If no such value is defined, an empty string is returned.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_bidirectional_impl(PyObject *self, int chr)
/*[clinic end generated code: output=d36310ce2039bb92 input=b3d8f42cebfcf475]*/
{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getrecord_ex(c)->bidirectional;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
            index = 0; /* unassigned */
        else if (old->bidir_changed != 0xFF)
            index = old->bidir_changed;
    }
    return PyUnicode_FromString(_PyUnicodePlus_BidirectionalNames[index]);
}

/*[clinic input]
unicodedata.UCD.combining -> int

    self: self
    chr: int(accept={str})
    /

Returns the canonical combining class assigned to the character chr as integer.

Returns 0 if no combining class is defined.
[clinic start generated code]*/

static int
unicodedata_UCD_combining_impl(PyObject *self, int chr)
/*[clinic end generated code: output=cad056d0cb6a5920 input=9f2d6b2a95d0a22a]*/
{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getrecord_ex(c)->combining;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
            index = 0; /* unassigned */
    }
    return index;
}

/*[clinic input]
unicodedata.UCD.mirrored -> int

    self: self
    chr: int(accept={str})
    /

Returns the mirrored property assigned to the character chr as integer.

Returns 1 if the character has been identified as a "mirrored"
character in bidirectional text, 0 otherwise.
[clinic start generated code]*/

static int
unicodedata_UCD_mirrored_impl(PyObject *self, int chr)
/*[clinic end generated code: output=2532dbf8121b50e6 input=5dd400d351ae6f3b]*/
{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getrecord_ex(c)->mirrored;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
            index = 0; /* unassigned */
        else if (old->mirrored_changed != 0xFF)
            index = old->mirrored_changed;
    }
    return index;
}

/*[clinic input]
unicodedata.UCD.east_asian_width

    self: self
    chr: int(accept={str})
    /

Returns the east asian width assigned to the character chr as string.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_east_asian_width_impl(PyObject *self, int chr)
/*[clinic end generated code: output=484e8537d9ee8197 input=c4854798aab026e0]*/
{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getrecord_ex(c)->east_asian_width;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
            index = 0; /* unassigned */
        else if (old->east_asian_width_changed != 0xFF)
            index = old->east_asian_width_changed;
    }
    return PyUnicode_FromString(_PyUnicodePlus_EastAsianWidthNames[index]);
}

/*[clinic input]
unicodedata.UCD.script

    self: self
    chr: int(accept={str})
    /

Returns the script of the character chr as string.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_script_impl(PyObject *self, int chr)
/*[clinic end generated code: output=b66bf2a44b193bbd input=b2d3d8b7c3f44c10]*/
{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getpropset_ex(c)->script;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
            index = 0; /* unassigned */
        else if (old->script_changed != 0xFF)
            index = old->script_changed;
    }
    return PyUnicode_FromString(_PyUnicodePlus_ScriptNames[index]);
}

/*[clinic input]
unicodedata.UCD.block

    self: self
    chr: int(accept={str})
    /

Returns the block of the character chr as string.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_block_impl(PyObject *self, int chr)
/*[clinic end generated code: output=d1a6fa2a441df78a input=cd752824be1b8313]*/
{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getpropset_ex(c)->block;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
            index = 0; /* unassigned */
        else if (old->block_changed != 0xFF)
            index = old->block_changed;
    }
    return PyUnicode_FromString(_PyUnicodePlus_BlockNames[index]);
}

/*[clinic input]
unicodedata.UCD.script_extensions

    self: self
    chr: int(accept={str})
    /

Returns the script extensions of the character chr as a list of strings.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_script_extensions_impl(PyObject *self, int chr)
/*[clinic end generated code: output=5f72d9e14acbb33b input=239d3b9b1519b7f9]*/
{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getpropset_ex(c)->script_extensions;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
            index = 0; /* unassigned */
        else if (old->script_extensions_changed != 0xFF)
            index = old->script_extensions_changed;
    }
    PyObject *scriptex_string = NULL;
    PyObject *divider = NULL;
    PyObject *se_list = NULL;
    if (!(scriptex_string = PyUnicode_FromString(_PyUnicodePlus_ScriptExtensionsSets[index]))) {
        goto exit;
    }
    if (!(divider = PyUnicode_FromString(" "))) {
        goto exit;
    }
    se_list = PyUnicode_Split(scriptex_string, divider, -1);

 exit:
    Py_CLEAR(divider);
    Py_CLEAR(scriptex_string);
    return se_list;
}

/*[clinic input]
unicodedata.UCD.indic_conjunct_break

    self: self
    chr: int(accept={str})
    /

Returns the Indic Conjunct Break category of the character chr as string.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_indic_conjunct_break_impl(PyObject *self, int chr)
/*[clinic end generated code: output=0c9e917743dd8ff3 input=e544000ccfd4e991]*/

{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getpropset_ex(c)->indic_conjunct_break;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
            index = 0; /* unassigned */
        else if (old->indic_conjunct_break_changed != 0xFF)
            index = old->indic_conjunct_break_changed;
    }
    return PyUnicode_FromString(_PyUnicodePlus_IndicConjunctBreakNames[index]);
}

/*[clinic input]
unicodedata.UCD.indic_positional_category

    self: self
    chr: int(accept={str})
    /

Returns the Indic Positional Category of the character chr as string.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_indic_positional_category_impl(PyObject *self, int chr)
/*[clinic end generated code: output=44d955f48cb0c0ae input=a4c97bb81c76cabb]*/
{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getpropset_ex(c)->indic_positional_category;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
            index = 0; /* unassigned */
        else if (old->indic_positional_category_changed != 0xFF)
            index = old->indic_positional_category_changed;
    }
    return PyUnicode_FromString(_PyUnicodePlus_IndicPositionalCategoryNames[index]);
}

/*[clinic input]
unicodedata.UCD.indic_syllabic_category

    self: self
    chr: int(accept={str})
    /

Returns the Indic Syllabic Category of the character chr as string.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_indic_syllabic_category_impl(PyObject *self, int chr)
/*[clinic end generated code: output=53cff8b0659473dd input=f361e4327f1f8df6]*/
{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getpropset_ex(c)->indic_syllabic_category;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
            index = 0; /* unassigned */
        else if (old->indic_syllabic_category_changed != 0xFF)
            index = old->indic_syllabic_category_changed;
    }
    return PyUnicode_FromString(_PyUnicodePlus_IndicSyllabicCategoryNames[index]);
}

/*[clinic input]
unicodedata.UCD.grapheme_cluster_break

    self: self
    chr: int(accept={str})
    /

Returns the Grapheme Cluster Break property of the character chr as string.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_grapheme_cluster_break_impl(PyObject *self, int chr)
/*[clinic end generated code: output=7c8f206a79cc1cd8 input=d255b81238031f5f]*/
{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getpropset_ex(c)->grapheme_cluster_break;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
            index = 0; /* unassigned */
        else if (old->grapheme_cluster_break_changed != 0xFF)
            index = old->grapheme_cluster_break_changed;
    }
    return PyUnicode_FromString(_PyUnicodePlus_GraphemeClusterBreakNames[index]);
}

/*[clinic input]
unicodedata.UCD.word_break

    self: self
    chr: int(accept={str})
    /

Returns the Word Break property of the character chr as string.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_word_break_impl(PyObject *self, int chr)
/*[clinic end generated code: output=c7dc4bfb8a58f7ec input=aa173ba46cc5393c]*/
{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getpropset_ex(c)->word_break;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
            index = 0; /* unassigned */
        else if (old->word_break_changed != 0xFF)
            index = old->word_break_changed;
    }
    return PyUnicode_FromString(_PyUnicodePlus_WordBreakNames[index]);
}

/*[clinic input]
unicodedata.UCD.sentence_break

    self: self
    chr: int(accept={str})
    /

Returns the Sentence Break property of the character chr as string.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_sentence_break_impl(PyObject *self, int chr)
/*[clinic end generated code: output=660396e821f6c079 input=b9f0f785ed99393a]*/
{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getpropset_ex(c)->sentence_break;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
            index = 0; /* unassigned */
        else if (old->sentence_break_changed != 0xFF)
            index = old->sentence_break_changed;
    }
    return PyUnicode_FromString(_PyUnicodePlus_SentenceBreakNames[index]);
}

/*[clinic input]
unicodedata.UCD.line_break

    self: self
    chr: int(accept={str})
    /

Returns the Line Break property of the character chr as string.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_line_break_impl(PyObject *self, int chr)
/*[clinic end generated code: output=54c6c702603901af input=856d2df6cb4b3159]*/
{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getpropset_ex(c)->line_break;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
            index = 0; /* unassigned */
        else if (old->line_break_changed != 0xFF)
            index = old->line_break_changed;
    }
    return PyUnicode_FromString(_PyUnicodePlus_LineBreakNames[index]);
}

/*[clinic input]
unicodedata.UCD.vertical_orientation

    self: self
    chr: int(accept={str})
    /

Returns the Vertical Orientation property of the character chr as string.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_vertical_orientation_impl(PyObject *self, int chr)
/*[clinic end generated code: output=3a85e1bcac1318d7 input=48c73d232b37cbe5]*/
{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getpropset_ex(c)->vertical_orientation;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
            index = 0; /* unassigned */
        else if (old->vertical_orientation_changed != 0xFF)
            index = old->vertical_orientation_changed;
    }
    return PyUnicode_FromString(_PyUnicodePlus_VerticalOrientationNames[index]);
}

/*[clinic input]
unicodedata.UCD.age

    self: self
    chr: int(accept={str})
    /

Returns the Age property of the character chr as string.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_age_impl(PyObject *self, int chr)
/*[clinic end generated code: output=65b9ca0dc56b5516 input=57aa81559ef3dc45]*/
{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getpropset_ex(c)->age;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
            index = 0; /* unassigned */
        else if (old->age_changed != 0xFF)
            index = old->age_changed;
    }
    return PyUnicode_FromString(_PyUnicodePlus_AgeNames[index]);
}

static PyObject *
_unicodedata_UCD_total_strokes_g_impl(PyObject *self, int chr)
{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getunihanset_ex(c)->total_strokes_g;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
            index = 0; /* unassigned */
        else if (old->total_strokes_g_changed != 0xFF)
            index = old->total_strokes_g_changed;
    }
    return PyLong_FromLong(index);
}

static PyObject *
_unicodedata_UCD_total_strokes_t_impl(PyObject *self, int chr)
{
    int index;
    Py_UCS4 c = (Py_UCS4)chr;
    index = (int) _getunihanset_ex(c)->total_strokes_t;
    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
            index = 0; /* unassigned */
        else if (old->total_strokes_t_changed != 0xFF)
            index = old->total_strokes_t_changed;
    }
    return PyLong_FromLong(index);
}

/*[clinic input]
unicodedata.UCD.total_strokes

    self: self
    chr: int(accept={str})
    /
    source: str(c_default="\"G\"") = "G"

Returns the total number of strokes of a character as integer. The optional 'source' argument allows one to specify 'G' (Simplified) or 'T' (Traditional) stroke counts (default 'G') 

If no such value is defined, returns 0.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_total_strokes_impl(PyObject *self, int chr,
                                   const char *source)
/*[clinic end generated code: output=7e0cd192bf7636fe input=63e03e8ca98c84d9]*/
{
    if (strcmp(source, "G") == 0) {
        return _unicodedata_UCD_total_strokes_g_impl(self, chr);
    }
    else if (strcmp(source, "T") == 0) {
        return _unicodedata_UCD_total_strokes_t_impl(self, chr);
    }
    else {
        PyErr_SetString(PyExc_ValueError, "source must be 'G' or 'T'");
        return NULL;
    }
}

/*[clinic input]
unicodedata.UCD.decomposition

    self: self
    chr: int(accept={str})
    /

Returns the character decomposition mapping assigned to the character chr as string.

An empty string is returned in case no such mapping is defined.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_decomposition_impl(PyObject *self, int chr)
/*[clinic end generated code: output=7d699f3ec7565d27 input=e4c12459ad68507b]*/
{
    char decomp[256];
    int code, index, count;
    size_t i;
    unsigned int prefix_index;
    Py_UCS4 c = (Py_UCS4)chr;

    code = (int)c;

    if (UCD_Check(self)) {
        const change_record *old = get_old_record(self, c);
        if (old->category_changed == 0)
#if PY_MINOR_VERSION < 13
        return PyUnicode_FromString(""); /* unassigned */
#else
        return Py_GetConstant(Py_CONSTANT_EMPTY_STR); /* unassigned */
#endif
    }

    if (code < 0 || code >= 0x110000)
        index = 0;
    else {
        index = decomp_index1[(code>>DECOMP_SHIFT)];
        index = decomp_index2[(index<<DECOMP_SHIFT)+
                             (code&((1<<DECOMP_SHIFT)-1))];
    }

    /* high byte is number of hex bytes (usually one or two), low byte
       is prefix code (from*/
    count = decomp_data[index] >> 8;

    /* XXX: could allocate the PyString up front instead
       (strlen(prefix) + 5 * count + 1 bytes) */

    /* Based on how index is calculated above and decomp_data is generated
       from Tools/unicode/makeunicodedata.py, it should not be possible
       to overflow decomp_prefix. */
    prefix_index = decomp_data[index] & 255;
    assert(prefix_index < Py_ARRAY_LENGTH(decomp_prefix));

    /* copy prefix */
    i = strlen(decomp_prefix[prefix_index]);
    memcpy(decomp, decomp_prefix[prefix_index], i);

    while (count-- > 0) {
        if (i)
            decomp[i++] = ' ';
        assert(i < sizeof(decomp));
        PyOS_snprintf(decomp + i, sizeof(decomp) - i, "%04X",
                      decomp_data[++index]);
        i += strlen(decomp + i);
    }
    return PyUnicode_FromStringAndSize(decomp, i);
}

static void
get_decomp_record(PyObject *self, Py_UCS4 code, 
                  int *index, int *prefix, int *count)
{
    if (code >= 0x110000) {
        *index = 0;
    }
    else if (UCD_Check(self) 
            && get_old_record(self, code)->category_changed==0) {
        /* unassigned in old version */
        *index = 0;
    }
    else {
        *index = decomp_index1[(code>>DECOMP_SHIFT)];
        *index = decomp_index2[(*index<<DECOMP_SHIFT)+
                               (code&((1<<DECOMP_SHIFT)-1))];
    }

    /* high byte is number of hex bytes (usually one or two), low byte
       is prefix code (from*/
    *count = decomp_data[*index] >> 8;
    *prefix = decomp_data[*index] & 255;

    (*index)++;
}

#define SBase   0xAC00
#define LBase   0x1100
#define VBase   0x1161
#define TBase   0x11A7
#define LCount  19
#define VCount  21
#define TCount  28
#define NCount  (VCount*TCount)
#define SCount  (LCount*NCount)

static PyObject*
nfd_nfkd(PyObject *self, PyObject *input, int k)
{
    PyObject *result;
    Py_UCS4 *output;
    Py_ssize_t i, o, osize;
    int kind;
    const void *data;
    /* Longest decomposition in Unicode 3.2: U+FDFA */
    Py_UCS4 stack[20];
    Py_ssize_t space, isize;
    int index, prefix, count, stackptr;
    unsigned char prev, cur;

    stackptr = 0;
    isize = PyUnicode_GET_LENGTH(input);
    space = isize;
    /* Overallocate at most 10 characters. */
    if (space > 10) {
        if (space <= PY_SSIZE_T_MAX - 10)
            space += 10;
    }
    else {
        space *= 2;
    }
    osize = space;
    output = PyMem_NEW(Py_UCS4, space);
    if (!output) {
        PyErr_NoMemory();
        return NULL;
    }
    i = o = 0;
    kind = PyUnicode_KIND(input);
    data = PyUnicode_DATA(input);

    while (i < isize) {
        stack[stackptr++] = PyUnicode_READ(kind, data, i++);
        while(stackptr) {
            Py_UCS4 code = stack[--stackptr];
            /* Hangul Decomposition adds three characters in
               a single step, so we need at least that much room. */
            if (space < 3) {
                Py_UCS4 *new_output;
                osize += 10;
                space += 10;
                new_output = PyMem_Realloc(output, osize*sizeof(Py_UCS4));
                if (new_output == NULL) {
                    PyMem_Free(output);
                    PyErr_NoMemory();
                    return NULL;
                }
                output = new_output;
            }
            /* Hangul Decomposition. */
            if (SBase <= code && code < (SBase+SCount)) {
                int SIndex = code - SBase;
                int L = LBase + SIndex / NCount;
                int V = VBase + (SIndex % NCount) / TCount;
                int T = TBase + SIndex % TCount;
                output[o++] = L;
                output[o++] = V;
                space -= 2;
                if (T != TBase) {
                    output[o++] = T;
                    space --;
                }
                continue;
            }
            /* normalization changes */
            if (UCD_Check(self)) {
                Py_UCS4 value = ((PreviousDBVersion*)self)->normalization(code);
                if (value != 0) {
                    stack[stackptr++] = value;
                    continue;
                }
            }

            /* Other decompositions. */
            get_decomp_record(self, code, &index, &prefix, &count);

            /* Copy character if it is not decomposable, or has a
               compatibility decomposition, but we do NFD. */
            if (!count || (prefix && !k)) {
                output[o++] = code;
                space--;
                continue;
            }
            /* Copy decomposition onto the stack, in reverse
               order.  */
            while(count) {
                code = decomp_data[index + (--count)];
                stack[stackptr++] = code;
            }
        }
    }

    result = PyUnicode_FromKindAndData(PyUnicode_4BYTE_KIND,
                                       output, o);
    PyMem_Free(output);
    if (!result)
        return NULL;
    /* result is guaranteed to be ready, as it is compact. */
    kind = PyUnicode_KIND(result);
    data = PyUnicode_DATA(result);

    /* Sort canonically. */
    i = 0;
    prev = _getrecord_ex(PyUnicode_READ(kind, data, i))->combining;
    for (i++; i < PyUnicode_GET_LENGTH(result); i++) {
        cur = _getrecord_ex(PyUnicode_READ(kind, data, i))->combining;
        if (prev == 0 || cur == 0 || prev <= cur) {
            prev = cur;
            continue;
        }
        /* Non-canonical order. Need to switch *i with previous. */
        o = i - 1;
        while (1) {
            Py_UCS4 tmp = PyUnicode_READ(kind, data, o+1);
            PyUnicode_WRITE(kind, data, o+1,
                            PyUnicode_READ(kind, data, o));
            PyUnicode_WRITE(kind, data, o, tmp);
            o--;
            if (o < 0)
                break;
            prev = _getrecord_ex(PyUnicode_READ(kind, data, o))->combining;
            if (prev == 0 || prev <= cur)
                break;
        }
        prev = _getrecord_ex(PyUnicode_READ(kind, data, i))->combining;
    }
    return result;
}

static int
find_nfc_index(const struct reindex* nfc, Py_UCS4 code)
{
    unsigned int index;
    for (index = 0; nfc[index].start; index++) {
        unsigned int start = nfc[index].start;
        if (code < start)
            return -1;
        if (code <= start + nfc[index].count) {
            unsigned int delta = code - start;
            return nfc[index].index + delta;
        }
    }
    return -1;
}

static PyObject*
nfc_nfkc(PyObject *self, PyObject *input, int k)
{
    PyObject *result;
    int kind;
    const void *data;
    Py_UCS4 *output;
    Py_ssize_t i, i1, o, len;
    int f,l,index,index1,comb;
    Py_UCS4 code;
    Py_ssize_t skipped[20];
    int cskipped = 0;

    result = nfd_nfkd(self, input, k);
    if (!result)
        return NULL;
    /* result will be "ready". */
    kind = PyUnicode_KIND(result);
    data = PyUnicode_DATA(result);
    len = PyUnicode_GET_LENGTH(result);

    /* We allocate a buffer for the output.
       If we find that we made no changes, we still return
       the NFD result. */
    output = PyMem_NEW(Py_UCS4, len);
    if (!output) {
        PyErr_NoMemory();
        Py_DECREF(result);
        return 0;
    }
    i = o = 0;

  again:
    while (i < len) {
      for (index = 0; index < cskipped; index++) {
          if (skipped[index] == i) {
              /* *i character is skipped.
                 Remove from list. */
              skipped[index] = skipped[cskipped-1];
              cskipped--;
              i++;
              goto again; /* continue while */
          }
      }
      /* Hangul Composition. We don't need to check for <LV,T>
         pairs, since we always have decomposed data. */
      code = PyUnicode_READ(kind, data, i);
      if (LBase <= code && code < (LBase+LCount) &&
          i + 1 < len &&
          VBase <= PyUnicode_READ(kind, data, i+1) &&
          PyUnicode_READ(kind, data, i+1) < (VBase+VCount)) {
          /* check L character is a modern leading consonant (0x1100 ~ 0x1112)
             and V character is a modern vowel (0x1161 ~ 0x1175). */
          int LIndex, VIndex;
          LIndex = code - LBase;
          VIndex = PyUnicode_READ(kind, data, i+1) - VBase;
          code = SBase + (LIndex*VCount+VIndex)*TCount;
          i+=2;
          if (i < len &&
              TBase < PyUnicode_READ(kind, data, i) &&
              PyUnicode_READ(kind, data, i) < (TBase+TCount)) {
              /* check T character is a modern trailing consonant
                 (0x11A8 ~ 0x11C2). */
              code += PyUnicode_READ(kind, data, i)-TBase;
              i++;
          }
          output[o++] = code;
          continue;
      }

      /* code is still input[i] here */
      f = find_nfc_index(nfc_first, code);
      if (f == -1) {
          output[o++] = code;
          i++;
          continue;
      }
      /* Find next unblocked character. */
      i1 = i+1;
      comb = 0;
      /* output base character for now; might be updated later. */
      output[o] = PyUnicode_READ(kind, data, i);
      while (i1 < len) {
          Py_UCS4 code1 = PyUnicode_READ(kind, data, i1);
          int comb1 = _getrecord_ex(code1)->combining;
          if (comb) {
              if (comb1 == 0)
                  break;
              if (comb >= comb1) {
                  /* Character is blocked. */
                  i1++;
                  continue;
              }
          }
          l = find_nfc_index(nfc_last, code1);
          /* i1 cannot be combined with i. If i1
             is a starter, we don't need to look further.
             Otherwise, record the combining class. */
          if (l == -1) {
            not_combinable:
              if (comb1 == 0)
                  break;
              comb = comb1;
              i1++;
              continue;
          }
          index = f*TOTAL_LAST + l;
          index1 = comp_index[index >> COMP_SHIFT];
          code = comp_data[(index1<<COMP_SHIFT)+
                           (index&((1<<COMP_SHIFT)-1))];
          if (code == 0)
              goto not_combinable;

          /* Replace the original character. */
          output[o] = code;
          /* Mark the second character unused. */
          assert(cskipped < 20);
          skipped[cskipped++] = i1;
          i1++;
          f = find_nfc_index(nfc_first, output[o]);
          if (f == -1)
              break;
      }
      /* Output character was already written.
         Just advance the indices. */
      o++; i++;
    }
    if (o == len) {
        /* No changes. Return original string. */
        PyMem_Free(output);
        return result;
    }
    Py_DECREF(result);
    result = PyUnicode_FromKindAndData(PyUnicode_4BYTE_KIND,
                                       output, o);
    PyMem_Free(output);
    return result;
}

// This needs to match the logic in makeunicodedata.py
// which constructs the quickcheck data.
typedef enum {YES = 0, MAYBE = 1, NO = 2} QuickcheckResult;

/* Run the Unicode normalization "quickcheck" algorithm.
 *
 * Return YES or NO if quickcheck determines the input is certainly
 * normalized or certainly not, and MAYBE if quickcheck is unable to
 * tell.
 *
 * If `yes_only` is true, then return MAYBE as soon as we determine
 * the answer is not YES.
 *
 * For background and details on the algorithm, see UAX #15:
 *   https://www.unicode.org/reports/tr15/#Detecting_Normalization_Forms
 */
static QuickcheckResult
is_normalized_quickcheck(PyObject *self, PyObject *input, bool nfc, bool k, 
                         bool yes_only)
{
    /* UCD 3.2.0 is requested, quickchecks must be disabled. */
    if (UCD_Check(self)) {
        return MAYBE;
    }

    if (PyUnicode_IS_ASCII(input)) {
        return YES;
    }

    Py_ssize_t i, len;
    int kind;
    const void *data;
    unsigned char prev_combining = 0;

    /* The two quickcheck bits at this shift have type QuickcheckResult. */
    int quickcheck_shift = (nfc ? 4 : 0) + (k ? 2 : 0);

    QuickcheckResult result = YES; /* certainly normalized, unless we find something */

    i = 0;
    kind = PyUnicode_KIND(input);
    data = PyUnicode_DATA(input);
    len = PyUnicode_GET_LENGTH(input);
    while (i < len) {
        Py_UCS4 ch = PyUnicode_READ(kind, data, i++);
        const _PyUnicodePlus_DatabaseRecord *record = _getrecord_ex(ch);

        unsigned char combining = record->combining;
        if (combining && prev_combining > combining)
            return NO; /* non-canonical sort order, not normalized */
        prev_combining = combining;

        unsigned char quickcheck_whole = record->normalization_quick_check;
        if (yes_only) {
            if (quickcheck_whole & (3 << quickcheck_shift))
                return MAYBE;
        } else {
            switch ((quickcheck_whole >> quickcheck_shift) & 3) {
            case NO:
              return NO;
            case MAYBE:
              result = MAYBE; /* this string might need normalization */
            }
        }
    }
    return result;
}

/*[clinic input]
unicodedata.UCD.is_normalized

    self: self
    form: unicode
    unistr as input: unicode
    /

Return whether the Unicode string unistr is in the normal form 'form'.

Valid values for form are 'NFC', 'NFKC', 'NFD', and 'NFKD'.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_is_normalized_impl(PyObject *self, PyObject *form,
                                   PyObject *input)
/*[clinic end generated code: output=11e5a3694e723ca5 input=a544f14cea79e508]*/
{
    if (PyUnicode_GET_LENGTH(input) == 0) {
        /* special case empty input strings. */
        Py_RETURN_TRUE;
    }

    PyObject *result;
    bool nfc = false;
    bool k = false;
    QuickcheckResult m;

    PyObject *cmp;
    int match = 0;

    if (PyUnicode_CompareWithASCIIString(form, "NFC") == 0) {
        nfc = true;
    }
    else if (PyUnicode_CompareWithASCIIString(form, "NFKC") == 0) {
        nfc = true;
        k = true;
    }
    else if (PyUnicode_CompareWithASCIIString(form, "NFD") == 0) {
        /* matches default values for `nfc` and `k` */
    }
    else if (PyUnicode_CompareWithASCIIString(form, "NFKD") == 0) {
        k = true;
    }
    else {
        PyErr_SetString(PyExc_ValueError, "invalid normalization form");
        return NULL;
    }

    m = is_normalized_quickcheck(self, input, nfc, k, false);

    if (m == MAYBE) {
        cmp = (nfc ? nfc_nfkc : nfd_nfkd)(self, input, k);
        if (cmp == NULL) {
            return NULL;
        }
        match = PyUnicode_Compare(input, cmp);
        Py_DECREF(cmp);
        result = (match == 0) ? Py_True : Py_False;
    }
    else {
        result = (m == YES) ? Py_True : Py_False;
    }

    return Py_NewRef(result);
}


/*[clinic input]
unicodedata.UCD.normalize

    self: self
    form: unicode
    unistr as input: unicode
    /

Return the normal form 'form' for the Unicode string unistr.

Valid values for form are 'NFC', 'NFKC', 'NFD', and 'NFKD'.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_normalize_impl(PyObject *self, PyObject *form,
                               PyObject *input)
/*[clinic end generated code: output=05ca4385a2ad6983 input=3a5206c0ad2833fb]*/
{
    if (PyUnicode_GET_LENGTH(input) == 0) {
        /* Special case empty input strings, since resizing
           them  later would cause internal errors. */
        return PyUnicode_FromObject(input);
    }

    if (PyUnicode_CompareWithASCIIString(form, "NFC") == 0) {
        if (is_normalized_quickcheck(self, input,
                                     true,  false, true) == YES) {
            return PyUnicode_FromObject(input);
        }
        return nfc_nfkc(self, input, 0);
    }
    if (PyUnicode_CompareWithASCIIString(form, "NFKC") == 0) {
        if (is_normalized_quickcheck(self, input,
                                     true,  true,  true) == YES) {
            return PyUnicode_FromObject(input);
        }
        return nfc_nfkc(self, input, 1);
    }
    if (PyUnicode_CompareWithASCIIString(form, "NFD") == 0) {
        if (is_normalized_quickcheck(self, input,
                                     false, false, true) == YES) {
            return PyUnicode_FromObject(input);
        }
        return nfd_nfkd(self, input, 0);
    }
    if (PyUnicode_CompareWithASCIIString(form, "NFKD") == 0) {
        if (is_normalized_quickcheck(self, input,
                                     false, true,  true) == YES) {
            return PyUnicode_FromObject(input);
        }
        return nfd_nfkd(self, input, 1);
    }
    PyErr_SetString(PyExc_ValueError, "invalid normalization form");
    return NULL;
}

/* -------------------------------------------------------------------- */
/* unicode character name tables */

/* data file generated by Tools/unicode/makeunicodedata.py */
#include "unicodename_db.h"

/* -------------------------------------------------------------------- */
/* database code (cut and pasted from the unidb package) */

static const char * const hangul_syllables[][3] = {
    { "G",  "A",   ""   },
    { "GG", "AE",  "G"  },
    { "N",  "YA",  "GG" },
    { "D",  "YAE", "GS" },
    { "DD", "EO",  "N", },
    { "R",  "E",   "NJ" },
    { "M",  "YEO", "NH" },
    { "B",  "YE",  "D"  },
    { "BB", "O",   "L"  },
    { "S",  "WA",  "LG" },
    { "SS", "WAE", "LM" },
    { "",   "OE",  "LB" },
    { "J",  "YO",  "LS" },
    { "JJ", "U",   "LT" },
    { "C",  "WEO", "LP" },
    { "K",  "WE",  "LH" },
    { "T",  "WI",  "M"  },
    { "P",  "YU",  "B"  },
    { "H",  "EU",  "BS" },
    { 0,    "YI",  "S"  },
    { 0,    "I",   "SS" },
    { 0,    0,     "NG" },
    { 0,    0,     "J"  },
    { 0,    0,     "C"  },
    { 0,    0,     "K"  },
    { 0,    0,     "T"  },
    { 0,    0,     "P"  },
    { 0,    0,     "H"  }
};

/* These ranges need to match makeunicodedata.py:cjk_ranges. */
static int
is_unified_ideograph(Py_UCS4 code)
{
    return
        (0x3400 <= code && code <= 0x4DBF)   || /* CJK Ideograph Extension A */
        (0x4E00 <= code && code <= 0x9FFF)   || /* CJK Ideograph */
        (0x20000 <= code && code <= 0x2A6DF) || /* CJK Ideograph Extension B */
        (0x2A700 <= code && code <= 0x2B739) || /* CJK Ideograph Extension C */
        (0x2B740 <= code && code <= 0x2B81D) || /* CJK Ideograph Extension D */
        (0x2B820 <= code && code <= 0x2CEA1) || /* CJK Ideograph Extension E */
        (0x2CEB0 <= code && code <= 0x2EBE0) || /* CJK Ideograph Extension F */
        (0x2EBF0 <= code && code <= 0x2EE5D) || /* CJK Ideograph Extension I */
        (0x30000 <= code && code <= 0x3134A) || /* CJK Ideograph Extension G */
        (0x31350 <= code && code <= 0x323AF);   /* CJK Ideograph Extension H */
}

/* macros used to determine if the given code point is in the PUA range that
 * we are using to store aliases and named sequences */
#define IS_ALIAS(cp) ((cp >= aliases_start) && (cp < aliases_end))
#define IS_NAMED_SEQ(cp) ((cp >= named_sequences_start) && \
                          (cp < named_sequences_end))


// DAWG decoding functions

static unsigned int
_dawg_decode_varint_unsigned(unsigned int index, unsigned int* result)
{
    unsigned int res = 0;
    unsigned int shift = 0;
    for (;;) {
        unsigned char byte = packed_name_dawg[index];
        res |= (byte & 0x7f) << shift;
        index++;
        shift += 7;
        if (!(byte & 0x80)) {
            *result = res;
            return index;
        }
    }
}

static int
_dawg_match_edge(const char* name, unsigned int namelen, unsigned int size,
                 unsigned int label_offset, unsigned int namepos)
{
    // This returns 1 if the edge matched, 0 if it didn't (but further edges
    // could match) and -1 if the name cannot match at all.
    if (size > 1 && namepos + size > namelen) {
        return 0;
    }
    for (unsigned int i = 0; i < size; i++) {
        if (packed_name_dawg[label_offset + i] != Py_TOUPPER(name[namepos + i])) {
            if (i > 0) {
                return -1; // cannot match at all
            }
            return 0;
        }
    }
    return 1;
}

// reading DAWG node information:
// a node is encoded by a varint. The lowest bit of that int is set if the node
// is a final, accepting state. The higher bits of that int represent the
// number of names that are encoded by the sub-DAWG started by this node. It's
// used to compute the position of a name.
//
// the starting node of the DAWG is at position 0.
//
// the varint representing a node is followed by the node's edges, the encoding
// is described below


static unsigned int
_dawg_decode_node(unsigned int node_offset, bool* final)
{
    unsigned int num;
    node_offset = _dawg_decode_varint_unsigned(node_offset, &num);
    *final = num & 1;
    return node_offset;
}

static bool
_dawg_node_is_final(unsigned int node_offset)
{
    unsigned int num;
    _dawg_decode_varint_unsigned(node_offset, &num);
    return num & 1;
}

static unsigned int
_dawg_node_descendant_count(unsigned int node_offset)
{
    unsigned int num;
    _dawg_decode_varint_unsigned(node_offset, &num);
    return num >> 1;
}


// reading DAWG edge information:
// a DAWG edge is comprised of the following information:
// (1) the size of the label of the string attached to the edge
// (2) the characters of that edge
// (3) the target node
// (4) whether the edge is the last edge in the list of edges following a node
//
// this information is encoded in a compact form as follows:
//
// +---------+-----------------+--------------+--------------------
// |  varint | size (if != 1)  | label chars  | ... next edge ...
// +---------+-----------------+--------------+--------------------
//
// - first comes a varint
//     - the lowest bit of that varint is whether the edge is final (4)
//     - the second lowest bit of that varint is true if the size of
//       the length of the label is 1 (1)
//     - the rest of the varint is an offset that can be used to compute
//       the offset of the target node of that edge (3)
//  - if the size is not 1, the first varint is followed by a
//    character encoding the number of characters of the label (1)
//    (unicode character names aren't larger than 256 bytes, therefore each
//    edge label can be at most 256 chars, but is usually smaller)
//  - the next size bytes are the characters of the label (2)
//
// the offset of the target node is computed as follows: the number in the
// upper bits of the varint needs to be added to the offset of the target node
// of the previous edge. For the first edge, where there is no previous target
// node, the offset of the first edge is used.
// The intuition here is that edges going out from a node often lead to nodes
// that are close by, leading to small offsets from the current node and thus
// fewer bytes.
//
// There is a special case: if a final node has no outgoing edges, it has to be
// followed by a 0 byte to indicate that there are no edges (because the end of
// the edge list is normally indicated in a bit in the edge encoding). This is
// indicated by _dawg_decode_edge returning -1


static int
_dawg_decode_edge(bool is_first_edge, unsigned int prev_target_node_offset,
                  unsigned int edge_offset, unsigned int* size,
                  unsigned int* label_offset, unsigned int* target_node_offset)
{
    unsigned int num;
    edge_offset = _dawg_decode_varint_unsigned(edge_offset, &num);
    if (num == 0 && is_first_edge) {
        return -1; // trying to decode past a final node without outgoing edges
    }
    bool last_edge = num & 1;
    num >>= 1;
    bool len_is_one = num & 1;
    num >>= 1;
    *target_node_offset = prev_target_node_offset + num;
    if (len_is_one) {
        *size = 1;
    } else {
        *size = packed_name_dawg[edge_offset++];
    }
    *label_offset = edge_offset;
    return last_edge;
}

static int
_lookup_dawg_packed(const char* name, unsigned int namelen)
{
    unsigned int stringpos = 0;
    unsigned int node_offset = 0;
    unsigned int result = 0; // this is the number of final nodes that we skipped to match name
    while (stringpos < namelen) {
        bool final;
        unsigned int edge_offset = _dawg_decode_node(node_offset, &final);
        unsigned int prev_target_node_offset = edge_offset;
        bool is_first_edge = true;
        for (;;) {
            unsigned int size;
            unsigned int label_offset, target_node_offset;
            int last_edge = _dawg_decode_edge(
                    is_first_edge, prev_target_node_offset, edge_offset,
                    &size, &label_offset, &target_node_offset);
            if (last_edge == -1) {
                return -1;
            }
            is_first_edge = false;
            prev_target_node_offset = target_node_offset;
            int matched = _dawg_match_edge(name, namelen, size, label_offset, stringpos);
            if (matched == -1) {
                return -1;
            }
            if (matched) {
                if (final)
                    result += 1;
                stringpos += size;
                node_offset = target_node_offset;
                break;
            }
            if (last_edge) {
                return -1;
            }
            result += _dawg_node_descendant_count(target_node_offset);
            edge_offset = label_offset + size;
        }
    }
    if (_dawg_node_is_final(node_offset)) {
        return result;
    }
    return -1;
}

static int
_inverse_dawg_lookup(char* buffer, unsigned int buflen, unsigned int pos)
{
    unsigned int node_offset = 0;
    unsigned int bufpos = 0;
    for (;;) {
        bool final;
        unsigned int edge_offset = _dawg_decode_node(node_offset, &final);

        if (final) {
            if (pos == 0) {
                if (bufpos + 1 == buflen) {
                    return 0;
                }
                buffer[bufpos] = '\0';
                return 1;
            }
            pos--;
        }
        unsigned int prev_target_node_offset = edge_offset;
        bool is_first_edge = true;
        for (;;) {
            unsigned int size;
            unsigned int label_offset, target_node_offset;
            int last_edge = _dawg_decode_edge(
                    is_first_edge, prev_target_node_offset, edge_offset,
                    &size, &label_offset, &target_node_offset);
            if (last_edge == -1) {
                return 0;
            }
            is_first_edge = false;
            prev_target_node_offset = target_node_offset;

            unsigned int descendant_count = _dawg_node_descendant_count(target_node_offset);
            if (pos < descendant_count) {
                if (bufpos + size >= buflen) {
                    return 0; // buffer overflow
                }
                for (unsigned int i = 0; i < size; i++) {
                    buffer[bufpos++] = packed_name_dawg[label_offset++];
                }
                node_offset = target_node_offset;
                break;
            } else if (!last_edge) {
                pos -= descendant_count;
                edge_offset = label_offset + size;
            } else {
                return 0;
            }
        }
    }
}


static int
_getucname(PyObject *self, 
           Py_UCS4 code, char* buffer, int buflen, int with_alias_and_seq)
{
    /* Find the name associated with the given code point.
     * If with_alias_and_seq is 1, check for names in the Private Use Area 15
     * that we are using for aliases and named sequences. */
    int offset;

    if (code >= 0x110000)
        return 0;

    /* XXX should we just skip all the code points in the PUAs here? */
    if (!with_alias_and_seq && (IS_ALIAS(code) || IS_NAMED_SEQ(code)))
        return 0;

    if (UCD_Check(self)) {
        /* in 3.2.0 there are no aliases and named sequences */
        const change_record *old;
        if (IS_ALIAS(code) || IS_NAMED_SEQ(code))
            return 0;
        old = get_old_record(self, code);
        if (old->category_changed == 0) {
            /* unassigned */
            return 0;
        }
    }

    if (SBase <= code && code < SBase+SCount) {
        /* Hangul syllable. */
        int SIndex = code - SBase;
        int L = SIndex / NCount;
        int V = (SIndex % NCount) / TCount;
        int T = SIndex % TCount;

        if (buflen < 27)
            /* Worst case: HANGUL SYLLABLE <10chars>. */
            return 0;
        strcpy(buffer, "HANGUL SYLLABLE ");
        buffer += 16;
        strcpy(buffer, hangul_syllables[L][0]);
        buffer += strlen(hangul_syllables[L][0]);
        strcpy(buffer, hangul_syllables[V][1]);
        buffer += strlen(hangul_syllables[V][1]);
        strcpy(buffer, hangul_syllables[T][2]);
        buffer += strlen(hangul_syllables[T][2]);
        *buffer = '\0';
        return 1;
    }

    if (is_unified_ideograph(code)) {
        if (buflen < 28)
            /* Worst case: CJK UNIFIED IDEOGRAPH-20000 */
            return 0;
        sprintf(buffer, "CJK UNIFIED IDEOGRAPH-%X", code);
        return 1;
    }

    /* get position of codepoint in order of names in the dawg */
    offset = dawg_codepoint_to_pos_index1[(code>>DAWG_CODEPOINT_TO_POS_SHIFT)];
    offset = dawg_codepoint_to_pos_index2[(offset<<DAWG_CODEPOINT_TO_POS_SHIFT) +
                               (code&((1<<DAWG_CODEPOINT_TO_POS_SHIFT)-1))];
    if (offset == DAWG_CODEPOINT_TO_POS_NOTFOUND)
        return 0;

    assert(buflen >= 0);
    return _inverse_dawg_lookup(buffer, Py_SAFE_DOWNCAST(buflen, int, unsigned int), offset);
}

static int
capi_getucname(Py_UCS4 code,
               char* buffer, int buflen,
               int with_alias_and_seq)
{
    return _getucname(NULL, code, buffer, buflen, with_alias_and_seq);

}

static void
find_syllable(const char *str, int *len, int *pos, int count, int column)
{
    int i, len1;
    *len = -1;
    for (i = 0; i < count; i++) {
        const char *s = hangul_syllables[i][column];
        len1 = Py_SAFE_DOWNCAST(strlen(s), size_t, int);
        if (len1 <= *len)
            continue;
        if (strncmp(str, s, len1) == 0) {
            *len = len1;
            *pos = i;
        }
    }
    if (*len == -1) {
        *len = 0;
    }
}

static int
_check_alias_and_seq(Py_UCS4* code, int with_named_seq)
{
    /* check if named sequences are allowed */
    if (!with_named_seq && IS_NAMED_SEQ(*code))
        return 0;
    /* if the code point is in the PUA range that we use for aliases,
     * convert it to obtain the right code point */
    if (IS_ALIAS(*code))
        *code = name_aliases[*code-aliases_start];
    return 1;
}


static int
_getcode(const char* name, int namelen, Py_UCS4* code)
{
    /* Return the code point associated with the given name.
     * Named aliases are not resolved, they are returned as a code point in the
     * PUA */

    /* Check for hangul syllables. */
    if (strncmp(name, "HANGUL SYLLABLE ", 16) == 0) {
        int len, L = -1, V = -1, T = -1;
        const char *pos = name + 16;
        find_syllable(pos, &len, &L, LCount, 0);
        pos += len;
        find_syllable(pos, &len, &V, VCount, 1);
        pos += len;
        find_syllable(pos, &len, &T, TCount, 2);
        pos += len;
        if (L != -1 && V != -1 && T != -1 && pos-name == namelen) {
            *code = SBase + (L*VCount+V)*TCount + T;
            return 1;
        }
        /* Otherwise, it's an illegal syllable name. */
        return 0;
    }

    /* Check for unified ideographs. */
    if (strncmp(name, "CJK UNIFIED IDEOGRAPH-", 22) == 0) {
        /* Four or five hexdigits must follow. */
        unsigned int v;
        v = 0;
        name += 22;
        namelen -= 22;
        if (namelen != 4 && namelen != 5)
            return 0;
        while (namelen--) {
            v *= 16;
            if (*name >= '0' && *name <= '9')
                v += *name - '0';
            else if (*name >= 'A' && *name <= 'F')
                v += *name - 'A' + 10;
            else
                return 0;
            name++;
        }
        if (!is_unified_ideograph(v))
            return 0;
        *code = v;
        return 1;
    }

    assert(namelen >= 0);
    int position = _lookup_dawg_packed(name, Py_SAFE_DOWNCAST(namelen, int, unsigned int));
    if (position < 0) {
        return 0;
    }
    *code = dawg_pos_to_codepoint[position];
    return 1;
}


static int
capi_getcode(const char* name, int namelen, Py_UCS4* code,
             int with_named_seq)
{
    if (!_getcode(name, namelen, code)) {
        return 0;
    }
    return _check_alias_and_seq(code, with_named_seq);
}

static void
unicodedata_destroy_capi(PyObject *capsule)
{
    void *capi = PyCapsule_GetPointer(capsule, PyUnicodeData_CAPSULE_NAME);
    PyMem_Free(capi);
}

static PyObject *
unicodedata_create_capi(void)
{
    _PyUnicode_Name_CAPI *capi = PyMem_Malloc(sizeof(_PyUnicode_Name_CAPI));
    if (capi == NULL) {
        PyErr_NoMemory();
        return NULL;
    }
    capi->getname = capi_getucname;
    capi->getcode = capi_getcode;

    PyObject *capsule = PyCapsule_New(capi,
                                      PyUnicodeData_CAPSULE_NAME,
                                      unicodedata_destroy_capi);
    if (capsule == NULL) {
        PyMem_Free(capi);
    }
    return capsule;
};


/* -------------------------------------------------------------------- */
/* Python bindings */

/*[clinic input]
unicodedata.UCD.name

    self: self
    chr: int(accept={str})
    default: object=NULL
    /

Returns the name assigned to the character chr as a string.

If no name is defined, default is returned, or, if not given,
ValueError is raised.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_name_impl(PyObject *self, int chr, PyObject *default_value)
/*[clinic end generated code: output=6bbb37a326407707 input=3e0367f534de56d9]*/
{
    char name[NAME_MAXLEN+1];
    Py_UCS4 c = (Py_UCS4)chr;

    if (!_getucname(self, c, name, NAME_MAXLEN, 0)) {
        if (default_value == NULL) {
            PyErr_SetString(PyExc_ValueError, "no such name");
            return NULL;
        }
        else {
            return Py_NewRef(default_value);
        }
    }

    return PyUnicode_FromString(name);
}

/*[clinic input]
unicodedata.UCD.lookup

    self: self
    name: str(accept={str, robuffer}, zeroes=True)
    /

Look up character by name.

If a character with the given name is found, return the
corresponding character.  If not found, KeyError is raised.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_lookup_impl(PyObject *self, const char *name,
                            Py_ssize_t name_length)
/*[clinic end generated code: output=7f03fc4959b242f6 input=a557be0f8607a0d6]*/
{
    Py_UCS4 code;
    unsigned int index;
    if (name_length > NAME_MAXLEN) {
        PyErr_SetString(PyExc_KeyError, "name too long");
        return NULL;
    }

    if (!_getcode(name, (int)name_length, &code)) {
        PyErr_Format(PyExc_KeyError, "undefined character name '%s'", name);
        return NULL;
    }
    if (UCD_Check(self)) {
        /* in 3.2.0 there are no aliases and named sequences */
        if (IS_ALIAS(code) || IS_NAMED_SEQ(code)) {
            PyErr_Format(PyExc_KeyError, "undefined character name '%s'", name);
            return 0;
        }
    }
    /* check if code is in the PUA range that we use for named sequences
       and convert it */
    if (IS_NAMED_SEQ(code)) {
        index = code-named_sequences_start;
        return PyUnicode_FromKindAndData(PyUnicode_2BYTE_KIND,
                                         named_sequences[index].seq,
                                         named_sequences[index].seqlen);
    }
    if (IS_ALIAS(code)) {
        code = name_aliases[code-aliases_start];
    }
    return PyUnicode_FromOrdinal(code);
}

/*[clinic input]
unicodedata.UCD.is_emoji

    self: self
    chr: int(accept={str})
    /

Returns True if chr is Emoji=Yes.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_is_emoji_impl(PyObject *self, int chr)
/*[clinic end generated code: output=c8198f08512ac46e input=b8cf9f213e8e44a5]*/
{
    Py_UCS4 c = (Py_UCS4)chr;
    if (_PyUnicodePlus_IsEmoji(c)) {
        Py_RETURN_TRUE;
    } else {
        Py_RETURN_FALSE;
    }
}

/*[clinic input]
unicodedata.UCD.is_emoji_presentation

    self: self
    chr: int(accept={str})
    /

Returns True if chr is Emoji_Presentation=Yes.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_is_emoji_presentation_impl(PyObject *self, int chr)
/*[clinic end generated code: output=c770f7a26779de70 input=f5d0f3e3f5133b0a]*/
{
    Py_UCS4 c = (Py_UCS4)chr;
    if (_PyUnicodePlus_IsEmojiPresentation(c)) {
        Py_RETURN_TRUE;
    } else {
        Py_RETURN_FALSE;
    }
}

/*[clinic input]
unicodedata.UCD.is_emoji_modifier

    self: self
    chr: int(accept={str})
    /

Returns True if chr is Emoji_Modifier=Yes.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_is_emoji_modifier_impl(PyObject *self, int chr)
/*[clinic end generated code: output=3c53d1032f4caa36 input=554f080907c42d32]*/
{
    Py_UCS4 c = (Py_UCS4)chr;
    if (_PyUnicodePlus_IsEmojiModifier(c)) {
        Py_RETURN_TRUE;
    } else {
        Py_RETURN_FALSE;
    }
}

/*[clinic input]
unicodedata.UCD.is_emoji_modifier_base

    self: self
    chr: int(accept={str})
    /

Returns True if chr is Emoji_Modifier_Base=Yes.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_is_emoji_modifier_base_impl(PyObject *self, int chr)
/*[clinic end generated code: output=b833341bb939eee4 input=f422772ff7f0b487]*/
{
    Py_UCS4 c = (Py_UCS4)chr;
    if (_PyUnicodePlus_IsEmojiModifierBase(c)) {
        Py_RETURN_TRUE;
    } else {
        Py_RETURN_FALSE;
    }
}

/*[clinic input]
unicodedata.UCD.is_emoji_component

    self: self
    chr: int(accept={str})
    /

Returns True if chr is Emoji_Component=Yes.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_is_emoji_component_impl(PyObject *self, int chr)
/*[clinic end generated code: output=b2563288f7cb2a5f input=57d8c229bf8f3878]*/
{
    Py_UCS4 c = (Py_UCS4)chr;
    if (_PyUnicodePlus_IsEmojiComponent(c)) {
        Py_RETURN_TRUE;
    } else {
        Py_RETURN_FALSE;
    }
}

/*[clinic input]
unicodedata.UCD.is_extended_pictographic

    self: self
    chr: int(accept={str})
    /

Returns True if chr is Extended_Pictographic=Yes.
[clinic start generated code]*/

static PyObject *
unicodedata_UCD_is_extended_pictographic_impl(PyObject *self, int chr)
/*[clinic end generated code: output=ab92c472815421ac input=947b988616dedef0]*/
{
    Py_UCS4 c = (Py_UCS4)chr;
    if (_PyUnicodePlus_IsExtendedPictographic(c)) {
        Py_RETURN_TRUE;
    } else {
        Py_RETURN_FALSE;
    }
}

static PyObject *
unicodedata_build_propval_aliases()
{
    PyObject *result = PyDict_New();
    if (!result)
        goto err;

    const char *current_prop = NULL, *current_value = NULL;
    PyObject *current_dict, *current_list;
    const _PyUnicodePlus_PropertyValueAlias *record = _PyUnicodePlus_PropertyValueAliases;
    for (; record->prop_ourname; record++) {
        if (!current_prop || 0 != strcmp(current_prop, record->prop_ourname)) {
            current_prop = record->prop_ourname;
            current_value = NULL;
            current_dict = PyDict_New();
            if (!current_dict)
                goto err;
            PyDict_SetItemString(result, current_prop, current_dict);
            Py_DECREF(current_dict);
        }

        if (!current_value || 0 != strcmp(current_value, record->value_shortname)) {
            current_value = record->value_shortname;
            current_list = PyList_New(0);
            if (!current_list)
                goto err;
            PyDict_SetItemString(current_dict, current_value, current_list);
            Py_DECREF(current_list);
        }

        PyObject *alias = PyUnicode_FromString(record->value_alias);
        if (!alias)
            goto err;
        PyList_Append(current_list, alias);
        Py_DECREF(alias);
    }
    return result;

  err:
    Py_XDECREF(result);
    return NULL;
}

static PyObject *
unicodedata_build_propval_by_alias()
{
    PyObject *result = PyDict_New();
    if (!result)
        goto err;

    const char *current_prop = NULL;
    PyObject *current_dict;
    const _PyUnicodePlus_PropertyValueAlias *record = _PyUnicodePlus_PropertyValueAliases;
    for (; record->prop_ourname; record++) {
        if (!current_prop || 0 != strcmp(current_prop, record->prop_ourname)) {
            current_prop = record->prop_ourname;
            current_dict = PyDict_New();
            if (!current_dict)
                goto err;
            PyDict_SetItemString(result, current_prop, current_dict);
            Py_DECREF(current_dict);
        }

        PyObject *shortname = PyUnicode_FromString(record->value_shortname);
        if (!shortname)
            goto err;
        PyDict_SetItemString(current_dict, record->value_alias, shortname);
        Py_DECREF(shortname);
    }
    return result;

  err:
    Py_XDECREF(result);
    return NULL;
}

/* XXX Add doc strings. */

// List of functions used to define module functions *AND* unicodedata.UCD
// methods. For module functions, self is the module. For UCD methods, self
// is an UCD instance. The UCD_Check() macro is used to check if self is
// an UCD instance.
static PyMethodDef unicodedata_functions[] = {
    UNICODEDATA_UCD_DECIMAL_METHODDEF
    UNICODEDATA_UCD_DIGIT_METHODDEF
    UNICODEDATA_UCD_NUMERIC_METHODDEF
    UNICODEDATA_UCD_CATEGORY_METHODDEF
    UNICODEDATA_UCD_BIDIRECTIONAL_METHODDEF
    UNICODEDATA_UCD_COMBINING_METHODDEF
    UNICODEDATA_UCD_MIRRORED_METHODDEF
    UNICODEDATA_UCD_EAST_ASIAN_WIDTH_METHODDEF
    UNICODEDATA_UCD_SCRIPT_METHODDEF
    UNICODEDATA_UCD_BLOCK_METHODDEF
    UNICODEDATA_UCD_SCRIPT_EXTENSIONS_METHODDEF
    UNICODEDATA_UCD_INDIC_CONJUNCT_BREAK_METHODDEF
    UNICODEDATA_UCD_INDIC_POSITIONAL_CATEGORY_METHODDEF
    UNICODEDATA_UCD_INDIC_SYLLABIC_CATEGORY_METHODDEF
    UNICODEDATA_UCD_GRAPHEME_CLUSTER_BREAK_METHODDEF
    UNICODEDATA_UCD_WORD_BREAK_METHODDEF
    UNICODEDATA_UCD_SENTENCE_BREAK_METHODDEF
    UNICODEDATA_UCD_LINE_BREAK_METHODDEF
    UNICODEDATA_UCD_VERTICAL_ORIENTATION_METHODDEF
    UNICODEDATA_UCD_AGE_METHODDEF
    UNICODEDATA_UCD_TOTAL_STROKES_METHODDEF
    UNICODEDATA_UCD_DECOMPOSITION_METHODDEF
    UNICODEDATA_UCD_NAME_METHODDEF
    UNICODEDATA_UCD_LOOKUP_METHODDEF
    UNICODEDATA_UCD_IS_NORMALIZED_METHODDEF
    UNICODEDATA_UCD_NORMALIZE_METHODDEF
    UNICODEDATA_UCD_IS_EMOJI_METHODDEF
    UNICODEDATA_UCD_IS_EMOJI_PRESENTATION_METHODDEF
    UNICODEDATA_UCD_IS_EMOJI_MODIFIER_METHODDEF
    UNICODEDATA_UCD_IS_EMOJI_MODIFIER_BASE_METHODDEF
    UNICODEDATA_UCD_IS_EMOJI_COMPONENT_METHODDEF
    UNICODEDATA_UCD_IS_EXTENDED_PICTOGRAPHIC_METHODDEF


    {NULL, NULL}                /* sentinel */
};

#if PY_MINOR_VERSION < 10
static PyTypeObject UCD_Type = {
        /* The ob_type field must be initialized in the module init function
         * to be portable to Windows without using C++. */
        PyVarObject_HEAD_INIT(NULL, 0)
        "unicodedataplus.UCD",              /*tp_name*/
        sizeof(PreviousDBVersion),      /*tp_basicsize*/
        0,                      /*tp_itemsize*/
        /* methods */
        (destructor)PyObject_Del, /*tp_dealloc*/
        0,                      /*tp_vectorcall_offset*/
        0,                      /*tp_getattr*/
        0,                      /*tp_setattr*/
        0,                      /*tp_as_async*/
        0,                      /*tp_repr*/
        0,                      /*tp_as_number*/
        0,                      /*tp_as_sequence*/
        0,                      /*tp_as_mapping*/
        0,                      /*tp_hash*/
        0,                      /*tp_call*/
        0,                      /*tp_str*/
        PyObject_GenericGetAttr,/*tp_getattro*/
        0,                      /*tp_setattro*/
        0,                      /*tp_as_buffer*/
        Py_TPFLAGS_DEFAULT,     /*tp_flags*/
        0,                      /*tp_doc*/
        0,                      /*tp_traverse*/
        0,                      /*tp_clear*/
        0,                      /*tp_richcompare*/
        0,                      /*tp_weaklistoffset*/
        0,                      /*tp_iter*/
        0,                      /*tp_iternext*/
        unicodedata_functions,  /*tp_methods*/
        DB_members,             /*tp_members*/
        0,                      /*tp_getset*/
        0,                      /*tp_base*/
        0,                      /*tp_dict*/
        0,                      /*tp_descr_get*/
        0,                      /*tp_descr_set*/
        0,                      /*tp_dictoffset*/
        0,                      /*tp_init*/
        0,                      /*tp_alloc*/
        0,                      /*tp_new*/
        0,                      /*tp_free*/
        0,                      /*tp_is_gc*/
};
#else
static int
ucd_traverse(PyObject *self, visitproc visit, void *arg)
{
    Py_VISIT(Py_TYPE(self));
    return 0;
}

static void
ucd_dealloc(PyObject *self)
{
    PyTypeObject *tp = Py_TYPE(self);
    PyObject_GC_UnTrack(self);
    PyObject_GC_Del(self);
    Py_DECREF(tp);
}

static PyType_Slot ucd_type_slots[] = {
    {Py_tp_dealloc, ucd_dealloc},
    {Py_tp_traverse, ucd_traverse},
    {Py_tp_getattro, PyObject_GenericGetAttr},
    {Py_tp_methods, unicodedata_functions},
    {Py_tp_members, DB_members},
    {0, 0}
};

static PyType_Spec ucd_type_spec = {
    .name = "unicodedataplus.UCD",
    .basicsize = sizeof(PreviousDBVersion),
    .flags = (Py_TPFLAGS_DEFAULT | Py_TPFLAGS_DISALLOW_INSTANTIATION |
              Py_TPFLAGS_HAVE_GC | Py_TPFLAGS_IMMUTABLETYPE),
    .slots = ucd_type_slots
};
#endif

PyDoc_STRVAR(unicodedata_docstring,
"This module provides access to the Unicode Character Database which\n\
defines character properties for all Unicode characters. The data in\n\
this database is based on the UnicodeData.txt file version\n\
" UNIDATA_VERSION " which is publicly available from ftp://ftp.unicode.org/.\n\
\n\
The module uses the same names and symbols as defined by the\n\
UnicodeData File Format " UNIDATA_VERSION ".");

#if PY_MINOR_VERSION < 10
static struct PyModuleDef unicodedatamodule = {
        PyModuleDef_HEAD_INIT,
        "unicodedataplus",
        unicodedata_docstring,
        -1,
        unicodedata_functions,
        NULL,
        NULL,
        NULL,
        NULL
};

PyMODINIT_FUNC
PyInit_unicodedataplus(void)
{
    PyObject *m, *v;

    Py_TYPE(&UCD_Type) = &PyType_Type;

    m = PyModule_Create(&unicodedatamodule);
    if (!m)
        return NULL;

    PyModule_AddStringConstant(m, "unidata_version", UNIDATA_VERSION);
    Py_INCREF(&UCD_Type);
    PyModule_AddObject(m, "UCD", (PyObject*)&UCD_Type);

    PyObject *propval_aliases = unicodedata_build_propval_aliases();
    if (!propval_aliases)
        return NULL;
    PyModule_AddObject(m, "property_value_aliases", propval_aliases);
    PyObject *propval_by_alias = unicodedata_build_propval_by_alias();
    if (!propval_by_alias)
        return NULL;
    PyModule_AddObject(m, "property_value_by_alias", propval_by_alias);

    /* Previous versions */
    v = new_previous_version("3.2.0", get_change_3_2_0, normalization_3_2_0,
                             propval_aliases, propval_by_alias);
    if (v != NULL)
        PyModule_AddObject(m, "ucd_3_2_0", v);

    return m;
}
#else
static int
unicodedata_exec(PyObject *module)
{
    if (PyModule_AddStringConstant(module, "unidata_version", UNIDATA_VERSION) < 0) {
        return -1;
    }

    PyTypeObject *ucd_type = (PyTypeObject *)PyType_FromSpec(&ucd_type_spec);
    if (ucd_type == NULL) {
        return -1;
    }

    if (PyModule_AddType(module, ucd_type) < 0) {
        Py_DECREF(ucd_type);
        return -1;
    }

    PyObject *propval_aliases = unicodedata_build_propval_aliases();
    if (!propval_aliases)
        return -1;
    PyModule_AddObject(module, "property_value_aliases", propval_aliases);
    PyObject *propval_by_alias = unicodedata_build_propval_by_alias();
    if (!propval_by_alias)
        return -1;
    PyModule_AddObject(module, "property_value_by_alias", propval_by_alias);

    // Unicode database version 3.2.0 used by the IDNA encoding
    PyObject *v;
    v = new_previous_version(ucd_type, "3.2.0",
                             get_change_3_2_0, normalization_3_2_0,
                             propval_aliases, propval_by_alias);
    Py_DECREF(ucd_type);
#if PY_MINOR_VERSION < 13
    if (v == NULL) {
        return -1;
    }
    if (PyModule_AddObject(module, "ucd_3_2_0", v) < 0) {
        Py_DECREF(v);
        return -1;
    }
#else
    if (PyModule_Add(module, "ucd_3_2_0", v) < 0) {
        return -1;
    }
    /* Export C API */
    if (PyModule_Add(module, "_ucnhash_CAPI", unicodedata_create_capi()) < 0) {
        return -1;
    }
#endif

    return 0;
}

static PyModuleDef_Slot unicodedata_slots[] = {
    {Py_mod_exec, unicodedata_exec},
#if PY_MINOR_VERSION >= 12
    {Py_mod_multiple_interpreters, Py_MOD_PER_INTERPRETER_GIL_SUPPORTED},
#endif
#if PY_MINOR_VERSION >= 13
    {Py_mod_gil, Py_MOD_GIL_NOT_USED},
#endif
    {0, NULL}
};

static struct PyModuleDef unicodedata_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "unicodedataplus",
    .m_doc = unicodedata_docstring,
    .m_size = 0,
    .m_methods = unicodedata_functions,
    .m_slots = unicodedata_slots,
};

PyMODINIT_FUNC
PyInit_unicodedataplus(void)
{
    return PyModuleDef_Init(&unicodedata_module);
}
#endif

/*
Local variables:
c-basic-offset: 4
indent-tabs-mode: nil
End:
*/
