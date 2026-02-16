/**
 * Design tokens matching policyengine-app-v2 design system.
 * Source: @policyengine/design-system/tokens
 */

export const colors = {
  primary: {
    50: '#E6FFFA',
    100: '#B2F5EA',
    200: '#81E6D9',
    300: '#4FD1C5',
    400: '#38B2AC',
    500: '#319795', // Main teal
    600: '#2C7A7B',
    700: '#285E61',
    800: '#234E52',
    900: '#1D4044',
  },
  gray: {
    50: '#F9FAFB',
    100: '#F2F4F7',
    200: '#E2E8F0',
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
    700: '#026AA2',
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
    title: '#000000',
    warning: '#d9480f',
  },
  background: {
    primary: '#FFFFFF',
    secondary: '#F5F9FF',
    tertiary: '#F1F5F9',
  },
  border: {
    light: '#E2E8F0',
    medium: '#CBD5E1',
    dark: '#94A3B8',
  },
  shadow: {
    light: 'rgba(16, 24, 40, 0.05)',
    medium: 'rgba(16, 24, 40, 0.1)',
    dark: 'rgba(16, 24, 40, 0.2)',
  },
} as const;

export const typography = {
  fontFamily: {
    primary: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    mono: "JetBrains Mono, 'Fira Code', Consolas, monospace",
    chart: "Inter, sans-serif",
  },
  fontSize: {
    xs: '12px',
    sm: '14px',
    base: '16px',
    md: '16px',
    lg: '18px',
    xl: '20px',
    '2xl': '24px',
    '3xl': '28px',
    '4xl': '32px',
  },
  fontWeight: {
    thin: 100,
    light: 300,
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
    extrabold: 800,
  },
  lineHeight: {
    none: 1,
    tight: 1.25,
    snug: 1.375,
    normal: 1.5,
    relaxed: 1.625,
    loose: 2,
  },
} as const;

export const spacing = {
  xs: '4px',
  sm: '8px',
  md: '12px',
  lg: '16px',
  xl: '20px',
  '2xl': '24px',
  '3xl': '32px',
  '4xl': '48px',
  '5xl': '64px',
  radius: {
    xs: '2px',
    sm: '4px',
    md: '6px',
    lg: '8px',
    xl: '12px',
    '2xl': '16px',
    '3xl': '24px',
    full: '9999px',
  },
  appShell: {
    header: {
      height: '58px',
      padding: '8px 16px',
    },
    navbar: {
      width: '300px',
    },
    footer: {
      height: '60px',
      padding: '12px 24px',
    },
    main: {
      padding: '24px',
    },
    container: '976px',
  },
} as const;

export const shadows = {
  xs: `0 1px 2px ${colors.shadow.light}`,
  sm: `0 1px 3px ${colors.shadow.medium}`,
  md: `0 4px 6px ${colors.shadow.medium}`,
  lg: `0 10px 15px ${colors.shadow.medium}`,
  xl: `0 20px 25px ${colors.shadow.medium}`,
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
  positive: colors.primary[500],
  negative: colors.gray[600],
} as const;

export const RECHARTS_FONT_STYLE = {
  fontFamily: typography.fontFamily.chart,
  fontSize: 14,
  fill: colors.text.secondary,
} as const;

export const TOOLTIP_STYLE = {
  backgroundColor: colors.background.primary,
  border: `1px solid ${colors.border.light}`,
  borderRadius: spacing.radius.md,
  padding: spacing.sm,
} as const;

export const chartStyle = {
  fontFamily: typography.fontFamily.chart,
  fontSize: 14,
  color: colors.text.primary,
  margin: { top: 20, right: 40, left: 80, bottom: 60 },
} as const;
