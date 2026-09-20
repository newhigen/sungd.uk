import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    link: z.string().url().optional(),
    link2: z.string().url().optional(),
    icon2: z.string().optional(),
    github: z.string().url().optional(),
    image: z.string().optional(),
    imageLight: z.string().optional(),
    dashboard: z.string().optional(),
    timeline: z.array(z.object({
      img: z.string(),
      label: z.string(),
      intent: z.string(),
    })).optional(),
    intro: z.object({
      summary: z.string().optional(),
      use: z.array(z.string()).default([]),
    }).optional(),
    category: z.string().default('개발·엔지니어링'),
    tags: z.array(z.string()).default([]),
    period: z.string().optional(),
    icon: z.string().optional(),
  }),
});

export const collections = { projects };
