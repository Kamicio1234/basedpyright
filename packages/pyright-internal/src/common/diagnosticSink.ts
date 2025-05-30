/*
 * diagnostics.ts
 * Copyright (c) Microsoft Corporation.
 * Licensed under the MIT license.
 * Author: Eric Traut
 *
 * Class that collects and deduplicates diagnostics.
 */

import { appendArray } from './collectionUtils';
import { DiagnosticLevel } from './configOptions';
import { assertNever } from './debug';
import { Diagnostic, DiagnosticAction, DiagnosticCategory } from './diagnostic';
import { convertOffsetsToRange } from './positionUtils';
import { hashString } from './stringUtils';
import { Range, TextRange } from './textRange';
import { TextRangeCollection } from './textRangeCollection';
import { Uri } from './uri/uri';

// Represents a collection of diagnostics within a file.
export interface FileDiagnostics {
    fileUri: Uri;
    cell: number | undefined;
    version: number | undefined;
    diagnostics: Diagnostic[];
    reason: 'analysis' | 'tracking';
}

export namespace FileDiagnostics {
    export function toJsonObj(fileDiag: FileDiagnostics): any {
        return {
            fileUri: fileDiag.fileUri.toJsonObj(),
            cell: fileDiag.cell,
            version: fileDiag.version,
            diagnostics: fileDiag.diagnostics.map((d) => d.toJsonObj()),
            reason: fileDiag.reason,
        };
    }

    export function fromJsonObj(fileDiagObj: any): FileDiagnostics {
        return {
            fileUri: Uri.fromJsonObj(fileDiagObj.fileUri),
            cell: fileDiagObj.cell,
            version: fileDiagObj.version,
            diagnostics: fileDiagObj.diagnostics.map((d: any) => Diagnostic.fromJsonObj(d)),
            reason: fileDiagObj.reason,
        };
    }
}

// Creates and tracks a list of diagnostics.
export class DiagnosticSink {
    private _diagnosticList: Diagnostic[];
    private _diagnosticMap: Map<string, Diagnostic>;

    constructor(diagnostics?: Diagnostic[]) {
        this._diagnosticList = diagnostics || [];
        this._diagnosticMap = new Map<string, Diagnostic>();
    }

    fetchAndClear() {
        const prevDiagnostics = this._diagnosticList;
        this._diagnosticList = [];
        this._diagnosticMap.clear();
        return prevDiagnostics;
    }

    addError(message: string, range: Range) {
        return this.addDiagnostic(new Diagnostic(DiagnosticCategory.Error, message, range));
    }

    addWarning(message: string, range: Range) {
        return this.addDiagnostic(new Diagnostic(DiagnosticCategory.Warning, message, range));
    }

    addInformation(message: string, range: Range) {
        return this.addDiagnostic(new Diagnostic(DiagnosticCategory.Information, message, range));
    }

    addHint(message: string, range: Range, action?: DiagnosticAction) {
        const diag = new Diagnostic(DiagnosticCategory.Hint, message, range);
        if (action) {
            diag.addAction(action);
        }
        return this.addDiagnostic(diag);
    }

    addDiagnostic(diag: Diagnostic) {
        // Create a unique key for the diagnostic to prevent
        // adding duplicates.
        const key =
            `${diag.range.start.line},${diag.range.start.character}-` +
            `${diag.range.end.line}-${diag.range.end.character}:${hashString(diag.message)}}`;
        if (!this._diagnosticMap.has(key)) {
            this._diagnosticList.push(diag);
            this._diagnosticMap.set(key, diag);
        }
        return diag;
    }

    addDiagnostics(diagsToAdd: Diagnostic[]) {
        appendArray(this._diagnosticList, diagsToAdd);
    }

    getErrors() {
        return this._diagnosticList.filter((diag) => diag.category === DiagnosticCategory.Error);
    }

    getWarnings() {
        return this._diagnosticList.filter((diag) => diag.category === DiagnosticCategory.Warning);
    }

    getInformation() {
        return this._diagnosticList.filter((diag) => diag.category === DiagnosticCategory.Information);
    }

    getHint() {
        return this._diagnosticList.filter((diag) => diag.category === DiagnosticCategory.Hint);
    }
}

// Specialized version of DiagnosticSink that works with TextRange objects
// and converts text ranges to line and column numbers.
export class TextRangeDiagnosticSink extends DiagnosticSink {
    private _lines: TextRangeCollection<TextRange>;

    constructor(lines: TextRangeCollection<TextRange>, diagnostics?: Diagnostic[]) {
        super(diagnostics);
        this._lines = lines;
    }

    addDiagnosticWithTextRange(level: DiagnosticLevel, message: string, range: TextRange) {
        const positionRange = convertOffsetsToRange(range.start, range.start + range.length, this._lines);
        switch (level) {
            case 'error':
                return this.addError(message, positionRange);

            case 'warning':
                return this.addWarning(message, positionRange);

            case 'information':
                return this.addInformation(message, positionRange);
            case 'hint':
                return this.addHint(message, positionRange);
            case 'none':
                //TODO: why is none even allowed here?
                throw new Error(`${level} is not expected value`);
            default:
                assertNever(level, `${level} is not expected value`);
        }
    }
}
