// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import rehypeMermaid from 'rehype-mermaid';
import remarkBlogHide from './src/plugins/remark-blog-hide.js';

// https://astro.build/config
export default defineConfig({
  site: 'https://sungd.uk',
  redirects: {
    '/resume': '/cv',
  },
  vite: {
    plugins: [tailwindcss()],
    server: {
      allowedHosts: ['localhost', '127.0.0.1', '.ts.net'],
    },
  },
  integrations: [
    mdx(),
    sitemap({
      // public/ 아래 정적 페이지라 Astro 라우트로 안 잡힌다
      customPages: ['https://sungd.uk/cv/', 'https://sungd.uk/cv/en/'],
    }),
  ],
  markdown: {
    remarkPlugins: [remarkBlogHide],
    rehypePlugins: [rehypeMermaid],
    shikiConfig: {
      themes: {
        light: 'github-light',
        dark: 'github-dark',
      },
      defaultColor: false,
    },
  },
});