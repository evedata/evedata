import { resolve } from "path";

import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";
import RailsPlugin from "vite-plugin-rails";

export default defineConfig({
  plugins: [
    tailwindcss(),
    RailsPlugin({
      envVars: { RAILS_ENV: "development" },
      envOptions: { defineOn: "import.meta.env" },
      fullReload: {
        additionalPaths: ["config/routes.rb", "app/components/**/*", "app/views/**/*"],
        delay: 300,
      },
    }),
  ],
  resolve: {
    alias: {
      "@assets": resolve(__dirname, "app/assets"),
    },
  },
});
