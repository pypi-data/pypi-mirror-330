export const name = "LinoEditor";

import React from "react";
import { RegisterImportPool, Component } from "./Base";
import { quillMention, quillToolbar } from "./quillmodules";

let ex; const exModulePromises = ex = {
    AbortController: import(/* webpackChunkName: "AbortController_LinoEditor" */"abort-controller"),
    prButton: import(/* webpackChunkName: "prButton_LinoEditor" */"primereact/button"),
    prEditor: import(/* webpackChunkName: "prEditor_LinoEditor" */"primereact/editor"),
    prDialog: import(/* webpackChunkName: "prDialog_LinoEditor" */"primereact/dialog"),
    i18n: import(/* webpackChunkName: "i18n_LinoEditor" */"./i18n"),
}
RegisterImportPool(ex);


export class LinoEditor extends Component {
    static requiredModules = ["AbortController", "prButton", "prEditor",
        "prDialog", "i18n"];
    static iPool = ex;
    async prepare() {
        this.controller = new this.ex.AbortController.default();
        this.ex.i18n = this.ex.i18n.default;
    }

    render () {
        if (!this.state.ready) return null;
        return <div className="l-editor"
            onKeyDown={(e) => {
                if ((e.ctrlKey || e.metaKey) && e.code === "KeyS") {
                    e.stopPropagation();
                    e.preventDefault();
                    this.props.onDone(e);
                } else e.stopPropagation();
            }}>
            <this.ex.prDialog.Dialog
                header={this.props.label}
                icons={<this.ex.prButton.Button
                    className="p-transparent-button"
                    style={{border: "0px", background: 'transparent', color: 'black'}}
                    onClick={(e) => {
                        this.props.onDone(e);
                    }}
                    icon="pi pi-save"
                    tooltip={this.ex.i18n.t("Save!")}
                    label=""/>}
                maximizable={true}
                modal={true}
                onHide={(e) => {
                    this.props.onClose(e);
                }}
                style={{width: "70vw", height: "85vw"}}
                contentStyle={{height: "100%"}}
                visible={this.props.visible}>
                <this.ex.prEditor.Editor
                    headerTemplate={quillToolbar.header}
                    modules={{mention: quillMention({
                        silentFetch: this.props.silentFetch,
                        signal: this.controller.signal,
                        mentionValues: this.props.mentionValues})}}
                    onTextChange={e => this.props.onTextChange(e)}
                    value={this.props.value}/>
            </this.ex.prDialog.Dialog>
        </div>
    }
}
