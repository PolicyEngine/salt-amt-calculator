/**
 * Introduction slide component - the landing page of the calculator.
 */

import { Box, Text, Card, Stack, List } from '@mantine/core';
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
              fontSize: typography.fontSize['3xl'],
              fontWeight: typography.fontWeight.bold,
              color: colors.primary[500],
              marginBottom: spacing.sm,
            }}
          >
            The SALTernative
          </Text>
          <Text
            style={{
              fontSize: typography.fontSize.xl,
              fontWeight: typography.fontWeight.medium,
              color: colors.text.primary,
              marginBottom: spacing.md,
            }}
          >
            SALT Cap and Alternative Minimum Tax Analysis
          </Text>
          <Text
            style={{
              fontSize: typography.fontSize.md,
              color: colors.text.secondary,
            }}
          >
            Explore how SALT cap reforms and AMT changes affect your taxes
          </Text>
        </Box>

        <Box
          style={{
            background: colors.background.secondary,
            padding: spacing.lg,
            borderRadius: '8px',
          }}
        >
          <Text
            style={{
              fontSize: typography.fontSize.md,
              fontWeight: typography.fontWeight.semibold,
              color: colors.text.primary,
              marginBottom: spacing.sm,
            }}
          >
            How to Use This Calculator
          </Text>
          <List spacing="sm">
            <List.Item>
              Enter your household details and income in the sidebar
            </List.Item>
            <List.Item>
              Select your preferred policy scenario to analyze
            </List.Item>
            <List.Item>
              Click "Calculate" to run the PolicyEngine simulation
            </List.Item>
            <List.Item>
              Navigate through the slides to explore your personalized tax analysis
            </List.Item>
          </List>
        </Box>

        <Box style={{ textAlign: 'center' }}>
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
