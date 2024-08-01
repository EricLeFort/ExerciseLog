// @ts-check

import eslint from "@eslint/js";
import tseslint from "typescript-eslint";

const error = 2;

export default [
  {
    "ignores": [
      "built",
    ]
  },
  eslint.configs.recommended,
  ...tseslint.configs.strict,
  ...tseslint.configs.stylistic,
  {
    "rules": {
      // This rule allows "_" placeholder variables
      // Note: disable the base rule as it can report incorrect errors
      "no-unused-vars": "off",
      "@typescript-eslint/no-unused-vars": [
        error, {
          "args": "all",
          "argsIgnorePattern": "^_",
          "varsIgnorePattern": "^_",
          "caughtErrorsIgnorePattern": "^_",
        },
      ],

      // These aren't necessarily bad (IMO)
      "@typescript-eslint/no-extraneous-class": "off",

      // Formatting
      "@typescript-eslint/indent": [error, 2],
      "id-length": [error, {"min": 1, "max": 35}],
      "camelcase": error,

      // Possible Problems (Basic)
      "array-callback-return": error,
      "constructor-super": error,
      "for-direction": error,
      "getter-return": error,
      "no-async-promise-executor": error,
      "no-await-in-loop": error,
      "no-class-assign": error,
      "no-compare-neg-zero": error,
      "no-cond-assign": error,
      "no-const-assign": error,
      "no-constant-binary-expression": error,
      "no-constant-condition": error,
      "no-constructor-return": error,
      "no-control-regex": error,
      "no-debugger": error,
      "no-dupe-args": error,
      "no-dupe-class-members": error,
      "no-dupe-else-if": error,
      "no-dupe-keys": error,
      "no-duplicate-case": error,
      "no-duplicate-imports": error,
      "no-empty-character-class": error,
      "no-empty-pattern": error,
      "no-ex-assign": error,
      "no-fallthrough": error,
      "no-func-assign": error,
      "no-import-assign": error,
      "no-inner-declarations": error,
      "no-invalid-regexp": error,
      "no-irregular-whitespace": error,
      "no-loss-of-precision": error,
      "no-misleading-character-class": error,
      "no-new-native-nonconstructor": error,
      "no-obj-calls": error,
      "no-promise-executor-return": error,
      "no-prototype-builtins": error,
      "no-self-assign": error,
      "no-self-compare": error,
      "no-setter-return": error,
      "no-sparse-arrays": error,
      "no-template-curly-in-string": error,
      "no-this-before-super": error,
      //"no-undef": error,
      "no-unexpected-multiline": error,
      "no-unmodified-loop-condition": error,
      "no-unreachable": error,
      "no-unreachable-loop": error,
      "no-unsafe-finally": error,
      "no-unsafe-negation": error,
      "no-unsafe-optional-chaining": error,
      "no-unused-private-class-members": error,
      "no-use-before-define": error,
      "no-useless-backreference": error,
      "require-atomic-updates": error,
      "use-isnan": error,
      "valid-typeof": error,

      // Possible Problems (extras)
      "block-scoped-var": error,
      "class-methods-use-this": error,
      "consistent-return": error,
      "default-case": error,
      "default-case-last": error,
      "default-param-last": error,
      "eqeqeq": error,
      "func-name-matching": error,
      "guard-for-in": error,

      // Code cleanliness + misc
      "consistent-this": error,
      "curly": error,
      "dot-notation": error,
      "func-style": [error, "declaration"],
      //"max-params": [error, 7],
      //"max-statements": [error, 25],
      "no-alert": error,
      "no-array-constructor": error,
      "no-bitwise": error, // There can be a place for these but it should be very intentional
      "no-caller": error,
      "no-case-declarations": error,
      "no-div-regex": error,
      "no-console": error,
      "no-else-return": error,
      "no-empty": error,
      "no-empty-function": error,
      "no-empty-static-block": error,
      "no-eq-null": error,
      "no-eval": error,
      "no-extend-native": error,
      "no-extra-bind": error,
      "no-extra-boolean-cast": error,
      "no-extra-label": error,
      "no-global-assign": error,
      "no-implicit-coercion": error,
      "no-implicit-globals": error,
      "no-implied-eval": error,
      //"no-invalid-this": error,
      "no-iterator": error,
      "no-label-var": error,
      "no-labels": error,
      "no-lone-blocks": error,
      "no-lonely-if": error,
      "no-loop-func": error,
      "no-multi-assign": error,
      "no-multi-str": error,
      "no-negated-condition": error,
      "no-nested-ternary": error,
      "no-new": error,
      "no-new-func": error,
      "no-new-wrappers": error,
      "no-nonoctal-decimal-escape": error,
      "no-object-constructor": error,
      "no-octal": error,
      "no-octal-escape": error,
      "no-proto": error,
      "no-redeclare": error,
      "no-regex-spaces": error,
      "no-restricted-exports": error,
      "no-restricted-globals": error,
      "no-restricted-imports": error,
      "no-restricted-properties": error,
      "no-restricted-syntax": error,
      "no-return-assign": error,
      "no-script-url": error,
      "no-sequences": error,
      "no-shadow": error,
      "no-shadow-restricted-names": error,
      "no-throw-literal": error,
      "no-undef-init": error,
      "no-undefined": error,
      "no-underscore-dangle": error,
      "no-unneeded-ternary": error,
      "no-unused-expressions": error,
      "no-useless-call": error,
      "no-useless-catch": error,
      "no-useless-computed-key": error,
      "no-useless-concat": error,
      "no-useless-constructor": error,
      "no-useless-escape": error,
      "no-useless-rename": error,
      "no-useless-return": error,
      "no-var": error,
      "no-void": error,
      "no-with": error,
      "object-shorthand": error,
      "operator-assignment": error,
      "prefer-const": error,
      "prefer-destructuring": error,
      "prefer-exponentiation-operator": error,
      "prefer-named-capture-group": error,
      "prefer-numeric-literals": error,
      "prefer-object-has-own": error,
      "prefer-object-spread": error,
      "prefer-promise-reject-errors": error,
      "prefer-regex-literals": error,
      "prefer-rest-params": error,
      "prefer-spread": error,
      "prefer-template": error,
      "radix": error,
      "require-unicode-regexp": error,
      "require-yield": error,
      "sort-imports": error,
      "sort-vars": error,
      "strict": error,
      "symbol-description": error,
      "vars-on-top": error,
      "yoda": error,
    },
    "settings": {
      "typescript": {
        project: ["tsconfig.json"],
      }
    }
  }
];