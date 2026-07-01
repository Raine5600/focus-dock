import fs from "fs";
import path from "path";
import { PRODUCT } from "./product";

export type DownloadFileKind = "pdf" | "formulas";

export function getProductFilePath(): string {
  return path.join(process.cwd(), "private", "downloads", PRODUCT.fileName);
}

export function getFormulasFilePath(): string {
  return path.join(process.cwd(), "private", "downloads", PRODUCT.formulasFileName);
}

export function productFileExists(): boolean {
  return fs.existsSync(getProductFilePath());
}

export function formulasFileExists(): boolean {
  return fs.existsSync(getFormulasFilePath());
}

export function resolveDownloadFile(fileParam: string | null): {
  kind: DownloadFileKind;
  filePath: string;
  fileName: string;
  contentType: string;
} | null {
  if (fileParam === "formulas") {
    if (!formulasFileExists()) return null;
    return {
      kind: "formulas",
      filePath: getFormulasFilePath(),
      fileName: PRODUCT.formulasFileName,
      contentType: "text/plain; charset=utf-8",
    };
  }

  if (!productFileExists()) return null;
  return {
    kind: "pdf",
    filePath: getProductFilePath(),
    fileName: PRODUCT.fileName,
    contentType: "application/pdf",
  };
}