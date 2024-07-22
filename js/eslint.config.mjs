// @ts-check

import eslint from "@eslint/js";
import tseslint from "typescript-eslint";

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
        "error",
        {
          "args": "all",
          "argsIgnorePattern": "^_",
          "varsIgnorePattern": "^_",
          "caughtErrorsIgnorePattern": "^_",
        }
      ],
      "@typescript-eslint/indent": ["error", 2],
    },
    "settings": {
      "typescript": {
        project: ["tsconfig.json"],
      }
    }
  }
];