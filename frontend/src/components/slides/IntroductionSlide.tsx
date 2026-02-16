/**
 * Introduction slide component - the landing page of the calculator.
 */

import { Box, Text, Card, Stack } from '@mantine/core';
import { colors, spacing, typography } from '@/designTokens';

export function IntroductionSlide() {
  return (
    <Card
      style={{
        width: '100%',
        maxWidth: '900px',
        margin: '0 auto',
        padding: spacing.xl,
      }}
    >
      <Stack gap={spacing.lg}>
        <Box style={{ textAlign: 'center' }}>
          <Text
            style={{
              fontSize: typography.fontSize['4xl'],
              fontWeight: typography.fontWeight.bold,
              color: colors.text.primary,
              marginBottom: spacing.xs,
            }}
          >
            What&apos;s the{' '}
            <span
              style={{
                color: colors.primary[500],
                fontWeight: typography.fontWeight.bold,
                fontSize: 'inherit',
              }}
            >
              SALT
            </span>
            ernative?
          </Text>
        </Box>

        <Box
          style={{
            padding: spacing.lg,
            borderRadius: '8px',
          }}
        >
          <Text
            style={{
              fontSize: typography.fontSize.md,
              color: colors.text.secondary,
              fontStyle: 'italic',
              marginBottom: spacing.md,
            }}
          >
            The state and local tax (SALT) deduction and alternative minimum tax (AMT) are
            scheduled to change next year. We&apos;ll walk you through these policies and allow you
            to model your custom reform.
          </Text>
          <Text
            style={{
              fontSize: typography.fontSize.md,
              color: colors.text.primary,
              lineHeight: typography.lineHeight.relaxed,
            }}
          >
            This tool starts by describing the SALT deduction and AMT, both under{' '}
            <em>current law</em> (given the expiration of the Tax Cuts and Jobs Act (TCJA) in 2026)
            and under <em>current policy</em> (if the TCJA was extended beyond 2025). Then we&apos;ll
            explain these policies in the context of sample households. Finally, we&apos;ll put you in
            the driver&apos;s seat &mdash; you can design and simulate a range of SALT and AMT reforms,
            and we&apos;ll calculate how it affects the US and your household. Let&apos;s dive in!
          </Text>
        </Box>

        <Box style={{ textAlign: 'center', marginTop: spacing.md }}>
          <Text
            style={{
              fontSize: typography.fontSize.sm,
              color: colors.text.muted,
            }}
          >
            Powered by{' '}
            <Text
              component="span"
              style={{
                color: colors.primary[500],
                fontWeight: typography.fontWeight.semibold,
              }}
            >
              PolicyEngine
            </Text>
          </Text>
        </Box>
      </Stack>
    </Card>
  );
}
