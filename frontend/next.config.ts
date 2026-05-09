import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Mantine ships CJS interop; transpiling avoids ESM/CJS mismatch errors.
  transpilePackages: ['@mantine/core', '@mantine/hooks'],
  turbopack: {
    root: process.cwd(),
  },
};

export default nextConfig;
