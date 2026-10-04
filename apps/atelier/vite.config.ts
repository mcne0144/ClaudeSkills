import { defineConfig } from "vite";

// The knowledge base lives two levels up (ClaudeSkills/art-director) so the
// Claude Code skill and this app read the same files.
export default defineConfig({
  base: "./",
  server: { fs: { allow: ["..", "../.."] } },
  build: { outDir: "dist", chunkSizeWarningLimit: 2000 },
});
