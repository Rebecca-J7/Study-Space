// Provide a minimal JSX IntrinsicElements declaration to satisfy TypeScript
// errors when JSX types are not picked up automatically.
import * as React from "react";

declare global {
  namespace JSX {
    // Basic element and children types
    type Element = React.ReactElement<any, any> | null;
    interface IntrinsicElements {
      [elemName: string]: any;
    }
  }
}

export {};
