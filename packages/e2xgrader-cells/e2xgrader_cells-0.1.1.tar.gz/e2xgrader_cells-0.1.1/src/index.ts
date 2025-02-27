import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { NotebookPanel } from '@jupyterlab/notebook';
import { IEditorServices } from '@jupyterlab/codeeditor';

import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { E2XContentFactory } from './factory';

/**
 * Initialization data for the @e2xgrader/cells extension.
 */
const plugin: JupyterFrontEndPlugin<NotebookPanel.IContentFactory> = {
  id: '@e2xgrader/cells:factory',
  description: 'A JupyterLab extension.',
  autoStart: true,
  requires: [IEditorServices],
  optional: [ISettingRegistry],
  provides: NotebookPanel.IContentFactory,
  activate: async (
    _app: JupyterFrontEnd,
    editorServices: IEditorServices,
    settingRegistry: ISettingRegistry | null
  ) => {
    console.log('JupyterLab extension @e2xgrader/cells is activated!');
    const editorFactory = editorServices.factoryService.newInlineEditor;
    let contentFactory: E2XContentFactory;

    if (settingRegistry) {
      try {
        const settings = await settingRegistry.load(plugin.id);
        contentFactory = new E2XContentFactory({ editorFactory }, settings);
      } catch (reason) {
        console.error('Failed to load settings for @e2xgrader/cells', reason);
        contentFactory = new E2XContentFactory({ editorFactory });
      }
    } else {
      contentFactory = new E2XContentFactory({ editorFactory });
    }
    return contentFactory;
  }
};

export default plugin;
