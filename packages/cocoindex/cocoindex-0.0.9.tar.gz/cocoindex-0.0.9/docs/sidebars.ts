import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      collapsed: false,
      items: [
        'getting_started/overview',
        'getting_started/quickstart',
      ],
    },
    {
      type: 'category',
      label: 'CocoIndex Core',
      collapsed: false,
      items: [
        'core/concepts',
        'core/initialization',
        'core/flow_def',
        'core/cli',
        'core/custom_function',
      ],
    },
    {
      type: 'category',
      label: 'About',
      collapsed: false,
      items: [
        'about/community',
        'about/contributing',
      ],
    },
  ],
};

export default sidebars;