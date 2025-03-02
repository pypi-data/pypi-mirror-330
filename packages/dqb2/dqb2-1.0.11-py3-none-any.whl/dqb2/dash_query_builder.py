# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class dash_query_builder(Component):
    """A dash_query_builder component.
The Dash Query Builder component

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- alwaysShowActionButtons (boolean; default True):
    Whether to show action buttons all the time or just on hover.

- config (dict; optional):
    The config object. See the
    [Config](https://github.com/ukrbublik/react-awesome-query-builder/blob/master/CONFIG.adoc
    docs).

    `config` is a dict with keys:

    - settings (dict; required)

        `settings` is a dict with keys:

        - locale (dict; optional)

            `locale` is a dict with keys:

            - moment (string; optional)

            - antd (dict; optional)

                `antd` is a dict with keys:

                - constructor (optional):
                    The initial value of Object.prototype.constructor
                    is the standard built-in Object constructor.

                - toString (optional):
                    Returns a string representation of an object.

                - toLocaleString (optional):
                    Returns a date converted to a string using the
                    current locale.

                - valueOf (optional):
                    Returns the primitive value of the specified
                    object.

                - hasOwnProperty (optional):
                    Determines whether an object has a property with
                    the specified name. @,param,v, ,A property name.

                - isPrototypeOf (optional):
                    Determines whether an object exists in another
                    object's prototype chain. @,param,v, ,Another
                    object whose prototype chain is to be checked.

                - propertyIsEnumerable (optional):
                    Determines whether a specified property is
                    enumerable. @,param,v, ,A property name.

            - material (dict; optional)

                `material` is a dict with keys:

                - constructor (optional):
                    The initial value of Object.prototype.constructor
                    is the standard built-in Object constructor.

                - toString (optional):
                    Returns a string representation of an object.

                - toLocaleString (optional):
                    Returns a date converted to a string using the
                    current locale.

                - valueOf (optional):
                    Returns the primitive value of the specified
                    object.

                - hasOwnProperty (optional):
                    Determines whether an object has a property with
                    the specified name. @,param,v, ,A property name.

                - isPrototypeOf (optional):
                    Determines whether an object exists in another
                    object's prototype chain. @,param,v, ,Another
                    object whose prototype chain is to be checked.

                - propertyIsEnumerable (optional):
                    Determines whether a specified property is
                    enumerable. @,param,v, ,A property name.

            - mui (dict; optional)

                `mui` is a dict with keys:

                - constructor (optional):
                    The initial value of Object.prototype.constructor
                    is the standard built-in Object constructor.

                - toString (optional):
                    Returns a string representation of an object.

                - toLocaleString (optional):
                    Returns a date converted to a string using the
                    current locale.

                - valueOf (optional):
                    Returns the primitive value of the specified
                    object.

                - hasOwnProperty (optional):
                    Determines whether an object has a property with
                    the specified name. @,param,v, ,A property name.

                - isPrototypeOf (optional):
                    Determines whether an object exists in another
                    object's prototype chain. @,param,v, ,Another
                    object whose prototype chain is to be checked.

                - propertyIsEnumerable (optional):
                    Determines whether a specified property is
                    enumerable. @,param,v, ,A property name.

        - theme (dict; optional)

            `theme` is a dict with keys:

            - material (dict; optional)

                `material` is a dict with keys:

                - constructor (optional):
                    The initial value of Object.prototype.constructor
                    is the standard built-in Object constructor.

                - toString (optional):
                    Returns a string representation of an object.

                - toLocaleString (optional):
                    Returns a date converted to a string using the
                    current locale.

                - valueOf (optional):
                    Returns the primitive value of the specified
                    object.

                - hasOwnProperty (optional):
                    Determines whether an object has a property with
                    the specified name. @,param,v, ,A property name.

                - isPrototypeOf (optional):
                    Determines whether an object exists in another
                    object's prototype chain. @,param,v, ,Another
                    object whose prototype chain is to be checked.

                - propertyIsEnumerable (optional):
                    Determines whether a specified property is
                    enumerable. @,param,v, ,A property name.

            - mui (dict; optional)

                `mui` is a dict with keys:

                - constructor (optional):
                    The initial value of Object.prototype.constructor
                    is the standard built-in Object constructor.

                - toString (optional):
                    Returns a string representation of an object.

                - toLocaleString (optional):
                    Returns a date converted to a string using the
                    current locale.

                - valueOf (optional):
                    Returns the primitive value of the specified
                    object.

                - hasOwnProperty (optional):
                    Determines whether an object has a property with
                    the specified name. @,param,v, ,A property name.

                - isPrototypeOf (optional):
                    Determines whether an object exists in another
                    object's prototype chain. @,param,v, ,Another
                    object whose prototype chain is to be checked.

                - propertyIsEnumerable (optional):
                    Determines whether a specified property is
                    enumerable. @,param,v, ,A property name.

        - valueLabel (string; optional)

        - valuePlaceholder (string; optional)

        - fieldLabel (string; optional)

        - operatorLabel (string; optional)

        - fieldPlaceholder (string; optional)

        - funcPlaceholder (string; optional)

        - funcLabel (string; optional)

        - operatorPlaceholder (string; optional)

        - lockLabel (string; optional)

        - lockedLabel (string; optional)

        - deleteLabel (string; optional)

        - addGroupLabel (string; optional)

        - addCaseLabel (string; optional)

        - addDefaultCaseLabel (string; optional)

        - defaultCaseLabel (string; optional)

        - addRuleLabel (string; optional)

        - addSubRuleLabel (string; optional)

        - addSubGroupLabel (string; optional)

        - delGroupLabel (string; optional)

        - notLabel (string; optional)

        - fieldSourcesPopupTitle (string; optional)

        - valueSourcesPopupTitle (string; optional)

        - removeRuleConfirmOptions (dict; optional)

            `removeRuleConfirmOptions` is a dict with keys:

            - title (string; optional)

            - okText (string; optional)

            - okType (string; optional)

            - cancelText (string; optional)

        - removeGroupConfirmOptions (dict; optional)

            `removeGroupConfirmOptions` is a dict with keys:

            - title (string; optional)

            - okText (string; optional)

            - okType (string; optional)

            - cancelText (string; optional)

        - loadMoreLabel (string; optional)

        - loadingMoreLabel (string; optional)

        - typeToSearchLabel (string; optional)

        - loadingLabel (string; optional)

        - notFoundLabel (string; optional)

        - reverseOperatorsForNot (boolean; optional)

        - canShortMongoQuery (boolean; optional)

        - defaultField (string; optional)

        - defaultOperator (string; optional)

        - defaultConjunction (string; optional)

        - fieldSources (list of a value equal to: 'field', 'func's; optional)

        - valueSourcesInfo (dict; optional)

            `valueSourcesInfo` is a dict with keys:

            - field (dict; optional)

                `field` is a dict with keys:

                - label (string; required)

                - widget (string; optional)

            - func (dict; optional)

                `func` is a dict with keys:

                - label (string; required)

                - widget (string; optional)

            - value (dict; optional)

                `value` is a dict with keys:

                - label (string; required)

                - widget (string; optional)

            - const (dict; optional)

                `const` is a dict with keys:

                - label (string; required)

                - widget (string; optional)

        - canCompareFieldWithField (dict; optional)

            `canCompareFieldWithField` is a dict with keys:


        - canReorder (boolean; optional)

        - canRegroup (boolean; optional)

        - canRegroupCases (boolean; optional)

        - showNot (boolean; optional)

        - showLock (boolean; optional)

        - canDeleteLocked (boolean; optional)

        - maxNesting (number; optional)

        - setOpOnChangeField (list of a value equal to: 'default', 'keep', 'first', 'none's; required)

        - clearValueOnChangeField (boolean; optional)

        - clearValueOnChangeOp (boolean; optional)

        - canLeaveEmptyGroup (boolean; optional)

        - canLeaveEmptyCase (boolean; optional)

        - shouldCreateEmptyGroup (boolean; optional)

        - forceShowConj (boolean; optional)

        - immutableGroupsMode (boolean; optional)

        - immutableFieldsMode (boolean; optional)

        - immutableOpsMode (boolean; optional)

        - immutableValuesMode (boolean; optional)

        - maxNumberOfRules (dict; optional)

            `maxNumberOfRules` is a dict with keys:

            - toString (optional):
                Returns a string representation of an object.
                @,param,radix, ,Specifies a radix for converting
                numeric values to strings. This value is only used for
                numbers.

            - toFixed (required):
                Returns a string representing a number in fixed-point
                notation. @,param,fractionDigits, ,Number of digits
                after the decimal point. Must be in the range 0 - 20,
                inclusive.

            - toExponential (required):
                Returns a string containing a number represented in
                exponential notation. @,param,fractionDigits, ,Number
                of digits after the decimal point. Must be in the
                range 0 - 20, inclusive.

            - toPrecision (required):
                Returns a string containing a number represented
                either in exponential or fixed-point notation with a
                specified number of digits. @,param,precision, ,Number
                of significant digits. Must be in the range 1 - 21,
                inclusive.

            - valueOf (optional):
                Returns the primitive value of the specified object.

            - toLocaleString (dict; optional):
                Converts a number to a string by using the current or
                specified locale. @,param,locales, ,A locale string or
                array of locale strings that contain one or more
                language or locale tags. If you include more than one
                locale string, list them in descending order of
                priority so that the first entry is the preferred
                locale. If you omit this parameter, the default locale
                of the JavaScript runtime is used. @,param,options,
                ,An object that contains one or more properties that
                specify comparison options. @,param,locales, ,A locale
                string, array of locale strings, Intl.Locale object,
                or array of Intl.Locale objects that contain one or
                more language or locale tags. If you include more than
                one locale string, list them in descending order of
                priority so that the first entry is the preferred
                locale. If you omit this parameter, the default locale
                of the JavaScript runtime is used. @,param,options,
                ,An object that contains one or more properties that
                specify comparison options.

                `toLocaleString` is a dict with keys:


        - maxNumberOfCases (dict; optional)

            `maxNumberOfCases` is a dict with keys:

            - toString (optional):
                Returns a string representation of an object.
                @,param,radix, ,Specifies a radix for converting
                numeric values to strings. This value is only used for
                numbers.

            - toFixed (required):
                Returns a string representing a number in fixed-point
                notation. @,param,fractionDigits, ,Number of digits
                after the decimal point. Must be in the range 0 - 20,
                inclusive.

            - toExponential (required):
                Returns a string containing a number represented in
                exponential notation. @,param,fractionDigits, ,Number
                of digits after the decimal point. Must be in the
                range 0 - 20, inclusive.

            - toPrecision (required):
                Returns a string containing a number represented
                either in exponential or fixed-point notation with a
                specified number of digits. @,param,precision, ,Number
                of significant digits. Must be in the range 1 - 21,
                inclusive.

            - valueOf (optional):
                Returns the primitive value of the specified object.

            - toLocaleString (dict; optional):
                Converts a number to a string by using the current or
                specified locale. @,param,locales, ,A locale string or
                array of locale strings that contain one or more
                language or locale tags. If you include more than one
                locale string, list them in descending order of
                priority so that the first entry is the preferred
                locale. If you omit this parameter, the default locale
                of the JavaScript runtime is used. @,param,options,
                ,An object that contains one or more properties that
                specify comparison options. @,param,locales, ,A locale
                string, array of locale strings, Intl.Locale object,
                or array of Intl.Locale objects that contain one or
                more language or locale tags. If you include more than
                one locale string, list them in descending order of
                priority so that the first entry is the preferred
                locale. If you omit this parameter, the default locale
                of the JavaScript runtime is used. @,param,options,
                ,An object that contains one or more properties that
                specify comparison options.

                `toLocaleString` is a dict with keys:


        - showErrorMessage (boolean; optional)

        - convertableWidgets (dict with strings as keys and values of type list of strings; optional)

        - exportPreserveGroups (boolean; optional)

        - removeEmptyGroupsOnLoad (boolean; optional)

        - removeEmptyRulesOnLoad (boolean; optional)

        - removeIncompleteRulesOnLoad (boolean; optional)

        - removeInvalidMultiSelectValuesOnLoad (boolean; optional)

        - groupOperators (list of strings; optional)

        - useConfigCompress (boolean; optional)

        - keepInputOnChangeFieldSrc (boolean; optional)

        - fieldItemKeysForSearch (list of a value equal to: 'key', 'path', 'label', 'altLabel', 'tooltip', 'grouplabel's; optional)

        - listKeysForSearch (list of a value equal to: 'value', 'title', 'groupTitle's; optional)

        - sqlDialect (a value equal to: 'BigQuery', 'PostgreSQL', 'MySQL'; optional)

        - caseValueField (dict; optional)

            `caseValueField` is a dict with keys:

            - label2 (string; optional)

            - operators (list of strings; optional)

            - defaultOperator (string; optional)

            - excludeOperators (list of strings; optional)

            - type (string; required)

            - preferWidgets (list of strings; optional)

            - valueSources (list of a value equal to: 'field', 'func', 'value', 'const's; optional)

            - funcs (list of strings; optional)

            - tableName (string; optional)

            - fieldName (string; optional)

            - jsonLogicVar (string; optional)

            - fieldSettings (dict; optional)

                `fieldSettings` is a dict with keys:

    - min (number; optional)

    - max (number; optional)

    - step (number; optional)

    - marks (dict with strings as keys and values of type string; optional)

    - validateValue (dict; optional)

        `validateValue` is a dict with keys:


    - valuePlaceholder (string; optional)

                  Or dict with keys:

    - timeFormat (string; optional)

    - dateFormat (string; optional)

    - valueFormat (string; optional)

    - use12Hours (boolean; optional)

    - useKeyboard (boolean; optional)

    - validateValue (dict; optional)

        `validateValue` is a dict with keys:


    - valuePlaceholder (string; optional)

              Or dict with keys:

    - listValues (boolean

          Or number

      Or string | dict | list; optional)

    - allowCustomValues (boolean; optional)

    - showSearch (boolean; optional)

    - searchPlaceholder (string; optional)

    - showCheckboxes (boolean; optional)

    - asyncFetch (dict; optional)

        `asyncFetch` is a dict with keys:


    - useLoadMore (boolean; optional)

    - useAsyncSearch (boolean; optional)

    - forceAsyncSearch (boolean; optional)

    - fetchSelectedValuesOnInit (boolean; optional)

    - validateValue (dict; optional)

        `validateValue` is a dict with keys:


    - valuePlaceholder (string; optional) | dict with keys:

    - listValues (boolean | number | string | dict | list; optional)

    - allowCustomValues (boolean; optional)

    - showSearch (boolean; optional)

    - searchPlaceholder (string; optional)

    - showCheckboxes (boolean; optional)

    - asyncFetch (dict; optional)

        `asyncFetch` is a dict with keys:


    - useLoadMore (boolean; optional)

    - useAsyncSearch (boolean; optional)

    - forceAsyncSearch (boolean; optional)

    - fetchSelectedValuesOnInit (boolean; optional)

    - validateValue (dict; optional)

        `validateValue` is a dict with keys:


    - valuePlaceholder (string; optional) | dict with keys:

    - treeValues (dict; optional)

        `treeValues` is a dict with strings as keys and values of type
        dict with keys:

        - children (list of boolean | number | string | dict | lists; optional)

        - parent (boolean | number | string | dict | list; optional)

        - disabled (boolean; optional)

        - selectable (boolean; optional)

        - disableCheckbox (boolean; optional)

        - checkable (boolean; optional)

        - path (list of strings; optional)

        - value (string | number; required)

        - title (string; optional)

        - isCustom (boolean; optional)

        - isHidden (boolean; optional)

        - groupTitle (string; optional)

        - renderTitle (string; optional)

    - treeExpandAll (boolean; optional)

    - treeSelectOnlyLeafs (boolean; optional)

    - validateValue (dict; optional)

        `validateValue` is a dict with keys:


    - valuePlaceholder (string; optional) | dict with keys:

    - treeValues (dict; optional)

        `treeValues` is a dict with strings as keys and values of type
        dict with keys:

        - children (list of boolean | number | string | dict | lists; optional)

        - parent (boolean | number | string | dict | list; optional)

        - disabled (boolean; optional)

        - selectable (boolean; optional)

        - disableCheckbox (boolean; optional)

        - checkable (boolean; optional)

        - path (list of strings; optional)

        - value (string | number; required)

        - title (string; optional)

        - isCustom (boolean; optional)

        - isHidden (boolean; optional)

        - groupTitle (string; optional)

        - renderTitle (string; optional)

    - treeExpandAll (boolean; optional)

    - treeSelectOnlyLeafs (boolean; optional)

    - validateValue (dict; optional)

        `validateValue` is a dict with keys:


    - valuePlaceholder (string; optional) | dict with keys:

    - labelYes (string; optional)

    - labelNo (string; optional)

    - validateValue (dict; optional)

        `validateValue` is a dict with keys:


    - valuePlaceholder (string; optional) | dict with keys:

    - maxLength (number; optional)

    - maxRows (number; optional)

    - validateValue (dict; optional)

        `validateValue` is a dict with keys:


    - valuePlaceholder (string; optional) | dict with keys:

    - validateValue (dict; optional)

        `validateValue` is a dict with keys:


    - valuePlaceholder (string; optional)

            - defaultValue (boolean | number | string | dict | list; optional)

            - widgets (dict; optional)

                `widgets` is a dict with strings as keys and values of
                type dict with keys:

    - widgetProps (boolean | number | string | dict | list; optional)

    - opProps (boolean | number | string | dict | list; optional)

    - operators (list of strings; optional)

    - defaultOperator (string; optional)

    - valueLabel (string; optional)

    - valuePlaceholder (string; optional)

            - mainWidgetProps (boolean | number | string | dict | list; optional)

            - hideForSelect (boolean; optional)

            - hideForCompare (boolean; optional)

            - listValues (boolean | number | string | dict | list; optional)

            - allowCustomValues (boolean; optional)

            - isSpelVariable (boolean; optional)

            - label (string; optional)

            - tooltip (string; optional)

        - fieldSeparator (string; optional)

        - fieldSeparatorDisplay (string; optional)

        - formatReverse (dict; optional)

            `formatReverse` is a dict with keys:


        - sqlFormatReverse (dict; optional)

            `sqlFormatReverse` is a dict with keys:


        - spelFormatReverse (dict; optional)

            `spelFormatReverse` is a dict with keys:


        - formatField (dict; optional)

            `formatField` is a dict with keys:


        - formatSpelField (dict; optional)

            `formatSpelField` is a dict with keys:


        - formatAggr (dict; optional)

            `formatAggr` is a dict with keys:


        - renderField (dict; optional)

            `renderField` is a dict with keys:


        - renderOperator (dict; optional)

            `renderOperator` is a dict with keys:


        - renderFunc (dict; optional)

            `renderFunc` is a dict with keys:


        - renderConjs (dict; optional)

            `renderConjs` is a dict with keys:


        - renderButton (dict; optional)

            `renderButton` is a dict with keys:


        - renderIcon (dict; optional)

            `renderIcon` is a dict with keys:


        - renderButtonGroup (dict; optional)

            `renderButtonGroup` is a dict with keys:


        - renderSwitch (dict; optional)

            `renderSwitch` is a dict with keys:


        - renderProvider (dict; optional)

            `renderProvider` is a dict with keys:


        - renderValueSources (dict; optional)

            `renderValueSources` is a dict with keys:


        - renderFieldSources (dict; optional)

            `renderFieldSources` is a dict with keys:


        - renderConfirm (dict; optional)

            `renderConfirm` is a dict with keys:


        - useConfirm (optional)

        - renderSize (a value equal to: 'small', 'large', 'medium'; optional)

        - renderItem (dict; optional)

            `renderItem` is a dict with keys:


        - dropdownPlacement (a value equal to: 'topLeft', 'topCenter', 'topRight', 'bottomLeft', 'bottomCenter', 'bottomRight'; optional)

        - groupActionsPosition (a value equal to: 'topLeft', 'topCenter', 'topRight', 'bottomLeft', 'bottomCenter', 'bottomRight'; optional)

        - showLabels (boolean; optional)

        - maxLabelsLength (number; optional)

        - customFieldSelectProps (dict; optional)

            `customFieldSelectProps` is a dict with strings as keys
            and values of type dict with keys:


        - customOperatorSelectProps (dict; optional)

            `customOperatorSelectProps` is a dict with strings as keys
            and values of type dict with keys:


        - renderBeforeWidget (dict; optional)

            `renderBeforeWidget` is a dict with keys:


        - renderAfterWidget (dict; optional)

            `renderAfterWidget` is a dict with keys:


        - renderBeforeActions (dict; optional)

            `renderBeforeActions` is a dict with keys:


        - renderAfterActions (dict; optional)

            `renderAfterActions` is a dict with keys:


        - renderBeforeCaseValue (dict; optional)

            `renderBeforeCaseValue` is a dict with keys:


        - renderAfterCaseValue (dict; optional)

            `renderAfterCaseValue` is a dict with keys:


        - renderRuleError (dict; optional)

            `renderRuleError` is a dict with keys:


        - renderSwitchPrefix (string; optional)

        - defaultSliderWidth (string; optional)

        - defaultSelectWidth (string; optional)

        - defaultSearchWidth (string; optional)

        - defaultMaxRows (number; optional)

    - operators (dict with strings as keys and values of type boolean | number | string | dict | list; required)

    - widgets (dict with strings as keys and values of type boolean | number | string | dict | list; required)

    - conjunctions (dict; required)

        `conjunctions` is a dict with strings as keys and values of
        type dict with keys:

        - label (string; required)

        - formatConj (dict; required)

            `formatConj` is a dict with keys:

        - sqlFormatConj (dict; required)

            `sqlFormatConj` is a dict with keys:

        - spelFormatConj (dict; required)

            `spelFormatConj` is a dict with keys:

        - mongoConj (string; required)

        - jsonLogicConj (string; optional)

        - sqlConj (string; optional)

        - spelConj (string; optional)

        - spelConjs (list of strings; optional)

        - reversedConj (string; optional)

    - types (dict; required)

        `types` is a dict with strings as keys and values of type dict
        with keys:

        - valueSources (list of a value equal to: 'field', 'func', 'value', 'const's; optional)

        - defaultOperator (string; optional)

        - widgets (dict; required)

            `widgets` is a dict with strings as keys and values of type

            dict with keys:

            - widgetProps (boolean | number | string | dict | list; optional)

            - opProps (boolean | number | string | dict | list; optional)

            - operators (list of strings; optional)

            - defaultOperator (string; optional)

            - valueLabel (string; optional)

            - valuePlaceholder (string; optional)

        - mainWidget (string; optional)

        - excludeOperators (list of strings; optional)

        - mainWidgetProps (boolean | number | string | dict | list; optional)

    - fields (dict; required)

        `fields` is a dict with strings as keys and values of type
        dict with keys:

        - label2 (string; optional)

        - operators (list of strings; optional)

        - defaultOperator (string; optional)

        - excludeOperators (list of strings; optional)

        - type (string; required)

        - preferWidgets (list of strings; optional)

        - valueSources (list of a value equal to: 'field', 'func', 'value', 'const's; optional)

        - funcs (list of strings; optional)

        - tableName (string; optional)

        - fieldName (string; optional)

        - jsonLogicVar (string; optional)

        - fieldSettings (dict; optional)

            `fieldSettings` is a dict with keys:

            - min (number; optional)

            - max (number; optional)

            - step (number; optional)

            - marks (dict with strings as keys and values of type string; optional)

            - validateValue (dict; optional)

                `validateValue` is a dict with keys:

            - valuePlaceholder (string; optional)

                  Or dict with keys:

            - timeFormat (string; optional)

            - dateFormat (string; optional)

            - valueFormat (string; optional)

            - use12Hours (boolean; optional)

            - useKeyboard (boolean; optional)

            - validateValue (dict; optional)

                `validateValue` is a dict with keys:

            - valuePlaceholder (string; optional)

              Or dict with keys:

            - listValues (boolean | number | string | dict | list; optional)

            - allowCustomValues (boolean; optional)

            - showSearch (boolean; optional)

            - searchPlaceholder (string; optional)

            - showCheckboxes (boolean; optional)

            - asyncFetch (dict; optional)

                `asyncFetch` is a dict with keys:

            - useLoadMore (boolean; optional)

            - useAsyncSearch (boolean; optional)

            - forceAsyncSearch (boolean; optional)

            - fetchSelectedValuesOnInit (boolean; optional)

            - validateValue (dict; optional)

                `validateValue` is a dict with keys:

            - valuePlaceholder (string; optional) | dict with keys:

            - listValues (boolean | number | string | dict | list; optional)

            - allowCustomValues (boolean; optional)

            - showSearch (boolean; optional)

            - searchPlaceholder (string; optional)

            - showCheckboxes (boolean; optional)

            - asyncFetch (dict; optional)

                `asyncFetch` is a dict with keys:

            - useLoadMore (boolean; optional)

            - useAsyncSearch (boolean; optional)

            - forceAsyncSearch (boolean; optional)

            - fetchSelectedValuesOnInit (boolean; optional)

            - validateValue (dict; optional)

                `validateValue` is a dict with keys:

            - valuePlaceholder (string; optional) | dict with keys:

            - treeValues (dict; optional)

                `treeValues` is a dict with strings as keys and values of type

                dict with keys:

                - children (list of boolean | number | string | dict | lists; optional)

                - parent (boolean | number | string | dict | list; optional)

                - disabled (boolean; optional)

                - selectable (boolean; optional)

                - disableCheckbox (boolean; optional)

                - checkable (boolean; optional)

                - path (list of strings; optional)

                - value (string | number; required)

                - title (string; optional)

                - isCustom (boolean; optional)

                - isHidden (boolean; optional)

                - groupTitle (string; optional)

                - renderTitle (string; optional)

            - treeExpandAll (boolean; optional)

            - treeSelectOnlyLeafs (boolean; optional)

            - validateValue (dict; optional)

                `validateValue` is a dict with keys:

            - valuePlaceholder (string; optional) | dict with keys:

            - treeValues (dict; optional)

                `treeValues` is a dict with strings as keys and values of type

                dict with keys:

                - children (list of boolean | number | string | dict | lists; optional)

                - parent (boolean | number | string | dict | list; optional)

                - disabled (boolean; optional)

                - selectable (boolean; optional)

                - disableCheckbox (boolean; optional)

                - checkable (boolean; optional)

                - path (list of strings; optional)

                - value (string | number; required)

                - title (string; optional)

                - isCustom (boolean; optional)

                - isHidden (boolean; optional)

                - groupTitle (string; optional)

                - renderTitle (string; optional)

            - treeExpandAll (boolean; optional)

            - treeSelectOnlyLeafs (boolean; optional)

            - validateValue (dict; optional)

                `validateValue` is a dict with keys:

            - valuePlaceholder (string; optional) | dict with keys:

            - labelYes (string; optional)

            - labelNo (string; optional)

            - validateValue (dict; optional)

                `validateValue` is a dict with keys:

            - valuePlaceholder (string; optional) | dict with keys:

            - maxLength (number; optional)

            - maxRows (number; optional)

            - validateValue (dict; optional)

                `validateValue` is a dict with keys:

            - valuePlaceholder (string; optional) | dict with keys:

            - validateValue (dict; optional)

                `validateValue` is a dict with keys:

            - valuePlaceholder (string; optional)

        - defaultValue (boolean | number | string | dict | list; optional)

        - widgets (dict; optional)

            `widgets` is a dict with strings as keys and values of type

            dict with keys:

            - widgetProps (boolean | number | string | dict | list; optional)

            - opProps (boolean | number | string | dict | list; optional)

            - operators (list of strings; optional)

            - defaultOperator (string; optional)

            - valueLabel (string; optional)

            - valuePlaceholder (string; optional)

        - mainWidgetProps (boolean | number | string | dict | list; optional)

        - hideForSelect (boolean; optional)

        - hideForCompare (boolean; optional)

        - listValues (boolean | number | string | dict | list; optional)

        - allowCustomValues (boolean; optional)

        - isSpelVariable (boolean; optional)

        - label (string; optional)

        - tooltip (string; optional)

    - funcs (dict with strings as keys and values of type boolean | number | string | dict | list; optional)

    - ctx (dict with strings as keys and values of type boolean | number | string | dict | list; required)

- dynamic (boolean; default False):
    Toggles whether the tree is updated automatically or through a
    button.

- elasticSearchFormat (dict; optional):
    ElasticSearch query object.

    `elasticSearchFormat` is a dict with keys:

    - constructor (optional):
        The initial value of Object.prototype.constructor is the
        standard built-in Object constructor.

    - toString (optional):
        Returns a string representation of an object.

    - toLocaleString (optional):
        Returns a date converted to a string using the current locale.

    - valueOf (optional):
        Returns the primitive value of the specified object.

    - hasOwnProperty (optional):
        Determines whether an object has a property with the specified
        name. @,param,v, ,A property name.

    - isPrototypeOf (optional):
        Determines whether an object exists in another object's
        prototype chain. @,param,v, ,Another object whose prototype
        chain is to be checked.

    - propertyIsEnumerable (optional):
        Determines whether a specified property is enumerable.
        @,param,v, ,A property name.

- fields (dict; required):
    The fields to populate the query builder. See the
    [Fields](https://github.com/ukrbublik/react-awesome-query-builder/blob/master/CONFIG.adoc#configfields)
    docs.

    `fields` is a dict with strings as keys and values of type dict
    with keys:

    - label2 (string; optional)

    - operators (list of strings; optional)

    - defaultOperator (string; optional)

    - excludeOperators (list of strings; optional)

    - type (string; required)

    - preferWidgets (list of strings; optional)

    - valueSources (list of a value equal to: 'field', 'func', 'value', 'const's; optional)

    - funcs (list of strings; optional)

    - tableName (string; optional)

    - fieldName (string; optional)

    - jsonLogicVar (string; optional)

    - fieldSettings (dict; optional)

        `fieldSettings` is a dict with keys:

        - min (number; optional)

        - max (number; optional)

        - step (number; optional)

        - marks (dict with strings as keys and values of type string; optional)

        - validateValue (dict; optional)

            `validateValue` is a dict with keys:

        - valuePlaceholder (string; optional)

              Or dict with keys:

        - timeFormat (string; optional)

        - dateFormat (string; optional)

        - valueFormat (string; optional)

        - use12Hours (boolean; optional)

        - useKeyboard (boolean; optional)

        - validateValue (dict; optional)

            `validateValue` is a dict with keys:

        - valuePlaceholder (string; optional)

      Or dict with keys:

        - listValues (boolean | number | string | dict | list; optional)

        - allowCustomValues (boolean; optional)

        - showSearch (boolean; optional)

        - searchPlaceholder (string; optional)

        - showCheckboxes (boolean; optional)

        - asyncFetch (dict; optional)

            `asyncFetch` is a dict with keys:

        - useLoadMore (boolean; optional)

        - useAsyncSearch (boolean; optional)

        - forceAsyncSearch (boolean; optional)

        - fetchSelectedValuesOnInit (boolean; optional)

        - validateValue (dict; optional)

            `validateValue` is a dict with keys:

        - valuePlaceholder (string; optional) | dict with keys:

        - listValues (boolean | number | string | dict | list; optional)

        - allowCustomValues (boolean; optional)

        - showSearch (boolean; optional)

        - searchPlaceholder (string; optional)

        - showCheckboxes (boolean; optional)

        - asyncFetch (dict; optional)

            `asyncFetch` is a dict with keys:

        - useLoadMore (boolean; optional)

        - useAsyncSearch (boolean; optional)

        - forceAsyncSearch (boolean; optional)

        - fetchSelectedValuesOnInit (boolean; optional)

        - validateValue (dict; optional)

            `validateValue` is a dict with keys:

        - valuePlaceholder (string; optional) | dict with keys:

        - treeValues (dict; optional)

            `treeValues` is a dict with strings as keys and values of type

            dict with keys:

            - children (list of boolean | number | string | dict | lists; optional)

            - parent (boolean | number | string | dict | list; optional)

            - disabled (boolean; optional)

            - selectable (boolean; optional)

            - disableCheckbox (boolean; optional)

            - checkable (boolean; optional)

            - path (list of strings; optional)

            - value (string | number; required)

            - title (string; optional)

            - isCustom (boolean; optional)

            - isHidden (boolean; optional)

            - groupTitle (string; optional)

            - renderTitle (string; optional)

        - treeExpandAll (boolean; optional)

        - treeSelectOnlyLeafs (boolean; optional)

        - validateValue (dict; optional)

            `validateValue` is a dict with keys:

        - valuePlaceholder (string; optional) | dict with keys:

        - treeValues (dict; optional)

            `treeValues` is a dict with strings as keys and values of type

            dict with keys:

            - children (list of boolean | number | string | dict | lists; optional)

            - parent (boolean | number | string | dict | list; optional)

            - disabled (boolean; optional)

            - selectable (boolean; optional)

            - disableCheckbox (boolean; optional)

            - checkable (boolean; optional)

            - path (list of strings; optional)

            - value (string | number; required)

            - title (string; optional)

            - isCustom (boolean; optional)

            - isHidden (boolean; optional)

            - groupTitle (string; optional)

            - renderTitle (string; optional)

        - treeExpandAll (boolean; optional)

        - treeSelectOnlyLeafs (boolean; optional)

        - validateValue (dict; optional)

            `validateValue` is a dict with keys:

        - valuePlaceholder (string; optional) | dict with keys:

        - labelYes (string; optional)

        - labelNo (string; optional)

        - validateValue (dict; optional)

            `validateValue` is a dict with keys:

        - valuePlaceholder (string; optional) | dict with keys:

        - maxLength (number; optional)

        - maxRows (number; optional)

        - validateValue (dict; optional)

            `validateValue` is a dict with keys:

        - valuePlaceholder (string; optional) | dict with keys:

        - validateValue (dict; optional)

            `validateValue` is a dict with keys:

        - valuePlaceholder (string; optional)

    - defaultValue (boolean | number | string | dict | list; optional)

    - widgets (dict; optional)

        `widgets` is a dict with strings as keys and values of type
        dict with keys:

        - widgetProps (boolean | number | string | dict | list; optional)

        - opProps (boolean | number | string | dict | list; optional)

        - operators (list of strings; optional)

        - defaultOperator (string; optional)

        - valueLabel (string; optional)

        - valuePlaceholder (string; optional)

    - mainWidgetProps (boolean | number | string | dict | list; optional)

    - hideForSelect (boolean; optional)

    - hideForCompare (boolean; optional)

    - listValues (boolean | number | string | dict | list; optional)

    - allowCustomValues (boolean; optional)

    - isSpelVariable (boolean; optional)

    - label (string; optional)

    - tooltip (string; optional)

- jsonLogicFormat (dict; optional):
    JSONLogic object.

    `jsonLogicFormat` is a dict with keys:

    - constructor (optional):
        The initial value of Object.prototype.constructor is the
        standard built-in Object constructor.

    - toString (optional):
        Returns a string representation of an object.

    - toLocaleString (optional):
        Returns a date converted to a string using the current locale.

    - valueOf (optional):
        Returns the primitive value of the specified object.

    - hasOwnProperty (optional):
        Determines whether an object has a property with the specified
        name. @,param,v, ,A property name.

    - isPrototypeOf (optional):
        Determines whether an object exists in another object's
        prototype chain. @,param,v, ,Another object whose prototype
        chain is to be checked.

    - propertyIsEnumerable (optional):
        Determines whether a specified property is enumerable.
        @,param,v, ,A property name.

- loadFormat (a value equal to: 'tree', 'jsonLogicFormat', 'spelFormat'; default 'tree'):
    The load format string. Changes the tree based on the
    corresponding prop change.

- mongoDBFormat (dict; optional):
    MongoDB query object.

    `mongoDBFormat` is a dict with keys:

    - constructor (optional):
        The initial value of Object.prototype.constructor is the
        standard built-in Object constructor.

    - toString (optional):
        Returns a string representation of an object.

    - toLocaleString (optional):
        Returns a date converted to a string using the current locale.

    - valueOf (optional):
        Returns the primitive value of the specified object.

    - hasOwnProperty (optional):
        Determines whether an object has a property with the specified
        name. @,param,v, ,A property name.

    - isPrototypeOf (optional):
        Determines whether an object exists in another object's
        prototype chain. @,param,v, ,Another object whose prototype
        chain is to be checked.

    - propertyIsEnumerable (optional):
        Determines whether a specified property is enumerable.
        @,param,v, ,A property name.

- queryBuilderFormat (dict; optional):
    Query Builder object.

    `queryBuilderFormat` is a dict with keys:

    - constructor (optional):
        The initial value of Object.prototype.constructor is the
        standard built-in Object constructor.

    - toString (optional):
        Returns a string representation of an object.

    - toLocaleString (optional):
        Returns a date converted to a string using the current locale.

    - valueOf (optional):
        Returns the primitive value of the specified object.

    - hasOwnProperty (optional):
        Determines whether an object has a property with the specified
        name. @,param,v, ,A property name.

    - isPrototypeOf (optional):
        Determines whether an object exists in another object's
        prototype chain. @,param,v, ,Another object whose prototype
        chain is to be checked.

    - propertyIsEnumerable (optional):
        Determines whether a specified property is enumerable.
        @,param,v, ,A property name.

- queryString (string; optional):
    Query string.

- spelFormat (string; optional):
    SPEL query string.

- sqlFormat (string; optional):
    The WHERE clause in SQL.

- theme (a value equal to: 'mui', 'material', 'antd', 'fluent', 'bootstrap', 'basic'; default 'bootstrap'):
    The theme/styling used.

- tree (boolean | number | string | dict | list; default emptyTree):
    The JSON representation of the tree."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dqb2'
    _type = 'dash_query_builder'
    @_explicitize_args
    def __init__(self, tree=Component.UNDEFINED, sqlFormat=Component.UNDEFINED, jsonLogicFormat=Component.UNDEFINED, queryBuilderFormat=Component.UNDEFINED, mongoDBFormat=Component.UNDEFINED, queryString=Component.UNDEFINED, elasticSearchFormat=Component.UNDEFINED, spelFormat=Component.UNDEFINED, fields=Component.REQUIRED, config=Component.UNDEFINED, dynamic=Component.UNDEFINED, loadFormat=Component.UNDEFINED, alwaysShowActionButtons=Component.UNDEFINED, theme=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'alwaysShowActionButtons', 'config', 'dynamic', 'elasticSearchFormat', 'fields', 'jsonLogicFormat', 'loadFormat', 'mongoDBFormat', 'queryBuilderFormat', 'queryString', 'spelFormat', 'sqlFormat', 'theme', 'tree']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'alwaysShowActionButtons', 'config', 'dynamic', 'elasticSearchFormat', 'fields', 'jsonLogicFormat', 'loadFormat', 'mongoDBFormat', 'queryBuilderFormat', 'queryString', 'spelFormat', 'sqlFormat', 'theme', 'tree']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['fields']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(dash_query_builder, self).__init__(**args)
