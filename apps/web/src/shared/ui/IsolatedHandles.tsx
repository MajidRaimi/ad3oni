import { Fragment, type ReactNode } from "react";

const handlePattern = /(@\w+)/g;
const isHandle = (part: string) => part.startsWith("@");

export const IsolatedHandles = ({ text }: { text: string }): ReactNode =>
  text.split(handlePattern).map((part, index) =>
    isHandle(part) ? (
      <bdi key={index}>{part}</bdi>
    ) : (
      <Fragment key={index}>{part}</Fragment>
    ),
  );
