import type { NextConfig } from 'next';

const basePath = process.env.NEXT_PUBLIC_BASE_PATH !== undefined
  ? process.env.NEXT_PUBLIC_BASE_PATH
  : '/us/salternative';


const nextConfig: NextConfig = {
  ...(basePath ? { basePath } : {}),
  env: { NEXT_PUBLIC_BASE_PATH: basePath },
  // Mantine ships CJS interop; transpiling avoids ESM/CJS mismatch errors.
  transpilePackages: ['@mantine/core', '@mantine/hooks'],
  turbopack: {
    root: process.cwd(),
  },
};

export default nextConfig;
