/**
 * Transition slide component - simple text-based slide for section transitions.
 */

import { Box, Text, Card } from '@mantine/core';
import { colors, spacing, typography } from '@/designTokens';

interface TransitionSlideProps {
  title: string;
  subtitle?: string;
}

export function TransitionSlide({ title, subtitle }: TransitionSlideProps) {
  return (
    <Card
      style={{
        width: '100%',
        maxWidth: '800px',
        padding: spacing['2xl'],
        textAlign: 'center',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '300px',
      }}
    >
      <Box>
        <Text
          style={{
            fontSize: typography.fontSize['2xl'],
            fontWeight: typography.fontWeight.semibold,
            color: colors.text.primary,
            marginBottom: subtitle ? spacing.md : 0,
          }}
        >
          {title}
        </Text>
        {subtitle && (
          <Text
            style={{
              fontSize: typography.fontSize.md,
              color: colors.text.secondary,
            }}
          >
            {subtitle}
          </Text>
        )}
      </Box>
    </Card>
  );
}
