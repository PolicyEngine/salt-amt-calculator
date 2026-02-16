/**
 * Slide navigation component with prev/next buttons.
 * Uses a 3-column grid so buttons stay in fixed positions regardless of title length.
 */

import { Button, Text, Box } from '@mantine/core';
import { IconChevronLeft, IconChevronRight } from '@tabler/icons-react';
import { useStore } from '@/store';
import { colors, spacing, typography } from '@/designTokens';

const SLIDE_TITLES = [
  'Introduction',
  'SALT and federal income tax',
  'SALT deduction comparison',
  'Taxable income and AMTI',
  'Regular tax and AMT',
  'Income tax comparison',
  'How does this vary with wages',
  'Effective SALT cap',
  'Regular tax and AMT by income',
  'Gap chart',
  'Marginal tax rate',
  'Effective SALT cap formula',
  'Tax savings from SALT',
  'How would you reform SALT/AMT?',
  'Budgetary impacts',
  'Distributional impacts',
  'Key takeaways',
];

const TOTAL_SLIDES = SLIDE_TITLES.length;

export function SlideNavigation() {
  const { slideIndex, nextSlide, prevSlide, hasCalculated } = useStore();

  const canGoBack = slideIndex > 0;
  const canGoForward = slideIndex < TOTAL_SLIDES - 1 && (slideIndex === 0 || hasCalculated);

  return (
    <Box
      style={{
        display: 'grid',
        gridTemplateColumns: '1fr auto 1fr',
        alignItems: 'center',
        padding: `${spacing.sm} ${spacing.lg}`,
        maxWidth: '900px',
        width: '100%',
        margin: '0 auto',
      }}
    >
      <div style={{ justifySelf: 'start' }}>
        <Button
          variant="subtle"
          leftSection={<IconChevronLeft size={18} />}
          onClick={prevSlide}
          disabled={!canGoBack}
          color="teal"
          styles={{
            root: {
              fontWeight: typography.fontWeight.medium,
              fontSize: typography.fontSize.sm,
            },
          }}
        >
          Previous
        </Button>
      </div>

      <div style={{ textAlign: 'center' }}>
        <Text
          style={{
            fontSize: typography.fontSize.sm,
            fontWeight: typography.fontWeight.medium,
            color: colors.text.primary,
          }}
        >
          {SLIDE_TITLES[slideIndex]}
        </Text>
        <Text
          style={{
            fontSize: typography.fontSize.xs,
            color: colors.text.tertiary,
          }}
        >
          {slideIndex + 1} of {TOTAL_SLIDES}
        </Text>
      </div>

      <div style={{ justifySelf: 'end' }}>
        <Button
          variant="subtle"
          rightSection={<IconChevronRight size={18} />}
          onClick={nextSlide}
          disabled={!canGoForward}
          color="teal"
          styles={{
            root: {
              fontWeight: typography.fontWeight.medium,
              fontSize: typography.fontSize.sm,
            },
          }}
        >
          Next
        </Button>
      </div>
    </Box>
  );
}
