import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://fanzinesjdr.vercel.app',
  integrations: [
    starlight({
      title: 'Fanzines JDR',
      description: 'Archives des revues et fanzines francophones de jeu de rôle.',
      defaultLocale: 'root',
      locales: {
        root: {
          label: 'Français',
          lang: 'fr-FR',
        },
      },
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/guillaumejay/fanzinesjdr',
        },
      ],
      sidebar: [
        { label: 'Accueil', link: '/' },
        {
          label: 'Fanzines',
          items: [{ autogenerate: { directory: 'fanzines' } }],
        },
      ],
    }),
  ],
});
