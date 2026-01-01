/**
 * Slide navigation component with prev/next buttons.
 */

import { Button, Group, Text, Box } from '@mantine/core';
import { IconChevronLeft, IconChevronRight } from '@tabler/icons-react';
import { useStore } from '@/store';
import { colors, spacing, typography } from '@/designTokens';

const SLIDE_TITLES = [
  'Introduction',
  'SALT and Federal Income Tax',
  'SALT Deduction Comparison',
  'Taxable Income and AMTI',
  'Regular Tax and AMT',
  'Income Tax Comparison',
  'How Does This Vary with Wages',
  'Effective SALT Cap',
  'Regular Tax and AMT by Income',
  'Gap Chart',
  'Marginal Tax Rate',
  'Effective SALT Cap Formula',
  'Tax Savings from SALT',
  'How Would You Reform SALT/AMT?',
  'Budgetary Impacts',
  'Distributional Impacts',
  'Key Takeaways',
];

const TOTAL_SLIDES = SLIDE_TITLES.length;

export function SlideNavigation() {
  const { slideIndex, nextSlide, prevSlide, hasCalculated } = useStore();

  const canGoBack = slideIndex > 0;
  const canGoForward = slideIndex < TOTAL_SLIDES - 1 && (slideIndex === 0 || hasCalculated);

  return (
    <Box
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: spacing.md,
        backgroundColor: colors.background.primary,
        borderRadius: spacing.radius.lg,
        boxShadow: '0 -2px 10px rgba(0, 0, 0, 0.05)',
      }}
    >
      <Button
        variant="subtle"
        leftSection={<IconChevronLeft size={20} />}
        onClick={prevSlide}
        disabled={!canGoBack}
        style={{
          color: canGoBack ? colors.primary[600] : colors.gray[400],
        }}
      >
        Previous
      </Button>

      <Group gap="xs">
        <Text
          style={{
            fontSize: typography.fontSize.md,
            fontWeight: typography.fontWeight.medium,
            color: colors.text.primary,
          }}
        >
          {SLIDE_TITLES[slideIndex]}
        </Text>
        <Text
          style={{
            fontSize: typography.fontSize.sm,
            color: colors.text.tertiary,
          }}
        >
          ({slideIndex + 1}/{TOTAL_SLIDES})
        </Text>
      </Group>

      <Button
        variant="subtle"
        rightSection={<IconChevronRight size={20} />}
        onClick={nextSlide}
        disabled={!canGoForward}
        style={{
          color: canGoForward ? colors.primary[600] : colors.gray[400],
        }}
      >
        Next
      </Button>
    </Box>
  );
}
