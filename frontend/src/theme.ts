/**
 * Mantine theme configuration for PolicyEngine design system.
 */

import { createTheme } from '@mantine/core';
import type { MantineColorsTuple } from '@mantine/core';
import { colors, typography } from './designTokens';

// Convert color scale to Mantine format
const primary: MantineColorsTuple = [
  colors.primary[50],
  colors.primary[100],
  colors.primary[200],
  colors.primary[300],
  colors.primary[400],
  colors.primary[500],
  colors.primary[600],
  colors.primary[700],
  colors.primary[800],
  colors.primary[900],
];

const gray: MantineColorsTuple = [
  colors.gray[50],
  colors.gray[100],
  colors.gray[200],
  colors.gray[300],
  colors.gray[400],
  colors.gray[500],
  colors.gray[600],
  colors.gray[700],
  colors.gray[800],
  colors.gray[900],
];

export const theme = createTheme({
  primaryColor: 'primary',
  colors: {
    primary,
    gray,
  },
  fontFamily: typography.fontFamily.primary,
  headings: {
    fontFamily: typography.fontFamily.primary,
    fontWeight: '600',
  },
  defaultRadius: 'md',
  components: {
    Button: {
      defaultProps: {
        radius: 'md',
      },
    },
    Input: {
      defaultProps: {
        radius: 'md',
      },
    },
    Card: {
      defaultProps: {
        radius: 'lg',
        shadow: 'xs',
      },
    },
    Select: {
      defaultProps: {
        radius: 'md',
      },
    },
    NumberInput: {
      defaultProps: {
        radius: 'md',
      },
    },
    Checkbox: {
      defaultProps: {
        radius: 'sm',
      },
    },
  },
});
