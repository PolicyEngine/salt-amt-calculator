/**
 * Design tokens matching policyengine-app-v2 design system.
 * Based on @policyengine/design-system/tokens
 */

export const colors = {
  primary: {
    50: '#F0FDFA',
    100: '#CCFBF1',
    200: '#99F6E4',
    300: '#5EEAD4',
    400: '#2DD4BF',
    500: '#319795', // Main teal
    600: '#0D9488',
    700: '#285E61',
    800: '#115E59',
    900: '#1D4044',
  },
  gray: {
    50: '#F9FAFB',
    100: '#F3F4F6',
    200: '#E5E7EB',
    300: '#D1D5DB',
    400: '#9CA3AF',
    500: '#6B7280',
    600: '#4B5563',
    700: '#344054',
    800: '#1F2937',
    900: '#101828',
  },
  blue: {
    50: '#F0F9FF',
    100: '#E0F2FE',
    200: '#BAE6FD',
    300: '#7DD3FC',
    400: '#38BDF8',
    500: '#0EA5E9',
    600: '#0284C7',
    700: '#0369A1',
    800: '#075985',
    900: '#0C4A6E',
  },
  success: '#22C55E',
  warning: '#FEC601',
  error: '#EF4444',
  info: '#1890FF',
  text: {
    primary: '#000000',
    secondary: '#5A5A5A',
    tertiary: '#9CA3AF',
    muted: '#9CA3AF',
    inverse: '#FFFFFF',
  },
  background: {
    primary: '#FFFFFF',
    secondary: '#F5F9FF',
    tertiary: '#F1F5F9',
  },
  border: {
    light: '#E5E7EB',
    medium: '#D1D5DB',
    dark: '#9CA3AF',
  },
} as const;

export const typography = {
  fontFamily: {
    primary: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    secondary: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    body: "'Inter', sans-serif",
    mono: "'JetBrains Mono', 'Fira Code', monospace",
    chart: "'Inter', sans-serif",
  },
  fontSize: {
    xs: '12px',
    sm: '14px',
    md: '16px',
    lg: '18px',
    xl: '20px',
    '2xl': '24px',
    '3xl': '28px',
    '4xl': '32px',
  },
  fontWeight: {
    light: 300,
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
  lineHeight: {
    tight: 1.2,
    normal: 1.5,
    relaxed: 1.75,
  },
} as const;

export const spacing = {
  xs: '4px',
  sm: '8px',
  md: '16px',
  lg: '24px',
  xl: '32px',
  '2xl': '48px',
  '3xl': '64px',
  radius: {
    xs: '2px',
    sm: '4px',
    md: '8px',
    lg: '12px',
    xl: '16px',
    '2xl': '24px',
    full: '9999px',
  },
  appShell: {
    header: {
      height: '58px',
    },
    navbar: {
      width: '300px',
    },
  },
} as const;

export const shadows = {
  xs: '0 1px 2px rgba(0, 0, 0, 0.05)',
  sm: '0 1px 3px rgba(0, 0, 0, 0.1)',
  md: '0 4px 6px rgba(0, 0, 0, 0.1)',
  lg: '0 10px 15px rgba(0, 0, 0, 0.1)',
  xl: '0 20px 25px rgba(0, 0, 0, 0.1)',
} as const;

// Chart-specific styling
export const chartColors = {
  primary: colors.primary[500],
  secondary: colors.blue[500],
  series: [
    colors.primary[500],
    colors.blue[500],
    colors.primary[700],
    colors.blue[700],
    colors.gray[500],
  ],
  positive: colors.success,
  negative: colors.error,
} as const;

export const chartStyle = {
  fontFamily: typography.fontFamily.chart,
  fontSize: 14,
  color: colors.text.primary,
  margin: { top: 20, right: 40, left: 80, bottom: 60 },
} as const;
