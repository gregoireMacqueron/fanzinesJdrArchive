import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema({
      extend: z.object({
        legacy_page_id: z.number().optional(),
        legacy_title: z.string().optional(),
        legacy_revision_id: z.number().optional(),
        legacy_revision_timestamp: z.string().optional(),
        legacy_author: z.string().optional(),
        source_format: z.literal('mediawiki').optional(),
      }),
    }),
  }),
};
