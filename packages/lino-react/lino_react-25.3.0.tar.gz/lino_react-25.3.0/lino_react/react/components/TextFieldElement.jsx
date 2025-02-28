import './TextFieldElement.css';

import React from "react";

import { RegisterImportPool } from "./Base";

import { quillMention, overrideImageButtonHandler,
    imageHandler, quillToolbar } from "./quillmodules";
import * as constants from "./constants";
import { LeafComponentInput } from "./LinoComponentUtils";
import { LinoEditor } from "./LinoEditor";

let ex; const exModulePromises = ex = {
    AbortController: import(/* webpackChunkName: "AbortController_TextFieldElement" */"abort-controller"),
    prButton: import(/* webpackChunkName: "prButton_TextFieldElement" */"primereact/button"),
    prEditor: import(/* webpackChunkName: "prEditor_TextFieldElement" */"primereact/editor"),
    prPanel: import(/* webpackChunkName: "prPanel_TextFieldElement" */"primereact/panel"),
    i18n: import(/* webpackChunkName: "i18n_TextFieldElement" */"./i18n"),
};RegisterImportPool(ex);


export class TextFieldElement extends LeafComponentInput {
    static requiredModules = ["AbortController", "prButton", "prEditor",
        "prPanel", "i18n"].concat(LeafComponentInput.requiredModules);
    static iPool = Object.assign(ex, LeafComponentInput.iPool.copy());
    constructor(props) {
        super(props);
        this.state = {...this.state, new_window: false,
                      plain: props.elem.field_options.format === "plain",
                      inGrid: props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TABLE,
                      key: this.c.newSlug().toString()}
        this.ownWindowButton = React.createRef();

        this.getLinoInput = this.getLinoInput.bind(this);
        this.innerHTML = this.innerHTML.bind(this);
        this.onDiagClose = this.onDiagClose.bind(this);
        this.onDiagDone = this.onDiagDone.bind(this);
        this.onTextChange = this.onTextChange.bind(this);
        this.onQuillLoad = this.onQuillLoad.bind(this);
        this.updateValue = this.updateValue.bind(this);
    }

    async prepare() {
        await super.prepare();
        this.ex.i18n = this.ex.i18n.default;
        this.mentionValues = {
            "@": [{ value: this.ex.i18n.t("Mention @People") }],
            "#": [{ value: this.ex.i18n.t("Tag #content") }]
        }
        this.controller = new this.ex.AbortController.default();
        this.refStoreType = this.props.elem.field_options.virtualField ? "virtual" : "";
        this.setLeafRef({input: true, type: this.refStoreType});
    }

    componentWillUnmount() {
        this.controller.abort();
        // delete this.c.dataContext.refStore[`${this.refStoreType}Leaves`][
        //     this.props.elem.name];
    }

    getLinoInput() {
        const quillStyle = {height: '100%'};
        const { APP } = this.c;
        const modules = {
            mention: quillMention({
                silentFetch: this.c.actionHandler.silentFetch,
                signal: this.controller.signal, mentionValues: this.mentionValues})
        }
        if (APP.state.site_data.installed_plugins.includes('uploads'))
            modules.imageDropAndPaste = {handler: imageHandler};
        // if (this.state.plain) {
        //     quillStyle.fontFamily = '"Courier New", Courier, monospace';
        //     modules.keyboard = {bindings: {tab: {key: 9,
        //         handler: (range, context) => {
        //             this.quill.insertText(range.index, "    ");
        //             return false;
        //         }
        //     }}}
        // }
        return <React.Fragment>
            <div className="l-editor"
                style={{position: "relative"}}
                onClick={e => {
                    e.stopPropagation();
                }}
                onKeyDown={(e) => {
                    if (!((e.ctrlKey || e.metaKey) && e.code === "KeyS"))
                        e.stopPropagation();
                }}>
                <this.ex.prEditor.Editor
                    headerTemplate={this.state.plain || this.props.elem.field_options.noEditorHeader || this.state.inGrid ? <span></span> : quillToolbar.headerMain({ref: this.ownWindowButton})}
                    key={this.state.key}
                    modules={modules}
                    onLoad={this.onQuillLoad}
                    onTextChange={this.onTextChange}
                    ref={(e) => this.inputEl = e}
                    style={quillStyle}
                    tabIndex={this.props.tabIndex}
                    value={this.getValue()}/>
            </div>
        </React.Fragment>
    }

    innerHTML() {
        if (this.props.elem.field_options.alwaysEditable) return this.getLinoInput();
        let innerHTML = super.innerHTML(constants.DANGEROUS_HTML);
        const gv = this.getValueByName;
        if (this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_DETAIL)
            innerHTML = <div dangerouslySetInnerHTML={{
                __html: gv(`${this.dataKey}_full_preview`) || gv(this.dataKey) || "\u00a0"}}/>;
        if (
            this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TABLE
        ) return innerHTML;
        return <this.ex.prPanel.Panel
            headerTemplate={<div className="p-panel-header">
                {this.props.elem.label}
                {!this.disabled() && <this.ex.prButton.Button
                    className="p-transparent-button"
                    style={{
                        border: "0px",
                        background: 'transparent',
                        color: 'black',
                    }}
                    onClick={(e) => {
                        e.stopPropagation();
                        this.setState({new_window: true});
                    }}
                    icon="pi pi-pencil"
                    tooltip={this.ex.i18n.t("Edit this text in own window")}
                    tooltipOptions={{position: 'left'}}
                    label=""/>}
            </div>}
            style={{display: "flex", flexDirection: "column", height: "100%"}}>
            {innerHTML}
        </this.ex.prPanel.Panel>
    }

    updateValue(value) {
        // console.log("20240919 updateValue", this.dataKey, this.state.plain, value);
        this.update({[this.dataKey]: value});
    }

    onDiagClose(e) {
        this.setState({new_window: false});
    }

    onDiagDone() {
        this.setState({new_window: false});
        this.submit();
    }

    onTextChange(e) {
        // cleans up the trailing new line (\n)
        const plainValue = e.textValue.slice(0, -1);
        let value = (this.state.plain ? plainValue : e.htmlValue ) || "";
        this.updateValue(value);
        this.setState({});
    }

    focus = () => {
        if (this.quill) this.quill.focus();
    }

    onQuillLoad() {
        this.quill = this.inputEl.getQuill();
        // console.log("20240922 onQuillLoad", this.dataKey, this.state.plain, this.getValue());
        if (this.tabIndexMatch()) this.focus();
        if (this.state.plain) { this.quill.setText(this.getValue() || ""); return;}
        if (this.props.elem.field_options.noEditorHeader || this.state.inGrid) return;
        if (this.c.APP.state.site_data.installed_plugins.includes('uploads'))
            overrideImageButtonHandler(this.quill);
        this.ownWindowButton.current.addEventListener("click", e => {
            e.stopPropagation();
            this.setState({new_window: true});
        });
    }

    render() {
        if (!this.state.ready) return null;
        // TODO: Do App Dialog for LinoEditor.
        return <React.Fragment>
            {super.render(!this.props.editing_mode && !this.props.elem.field_options.alwaysEditable)}
            <LinoEditor
                mentionValues={this.mentionValues}
                onTextChange={this.onTextChange}
                onClose={this.onDiagClose}
                onDone={this.onDiagDone}
                silentFetch={this.props.urlParams.controller.actionHandler.silentFetch}
                value={this.getValue()}
                visible={this.state.new_window}/>
        </React.Fragment>
    }
}


export const PreviewTextFieldElement = TextFieldElement;
