/**
 * Key Takeaways slide - summary of key points.
 */

import { Box, Text, Card, Stack, List } from '@mantine/core';
import { colors, spacing, typography } from '@/designTokens';

export function KeyTakeawaysSlide() {
  return (
    <Card
      style={{
        width: '100%',
        maxWidth: '800px',
        padding: spacing.xl,
      }}
    >
      <Stack gap={spacing.lg}>
        <Text
          style={{
            fontSize: typography.fontSize['2xl'],
            fontWeight: typography.fontWeight.semibold,
            color: colors.text.primary,
          }}
        >
          Key Takeaways
        </Text>

        <List spacing="md" size="lg">
          <List.Item>
            <Text style={{ fontSize: typography.fontSize.md, color: colors.text.primary }}>
              AMT creates an effective SALT cap
            </Text>
          </List.Item>
          <List.Item>
            <Text style={{ fontSize: typography.fontSize.md, color: colors.text.primary }}>
              This moves with the gap between regular tax and AMT (assuming no SALT), and the marginal tax rate
            </Text>
          </List.Item>
          <List.Item>
            <Text style={{ fontSize: typography.fontSize.md, color: colors.text.primary }}>
              <strong>Coming soon</strong>: how custom policies affect your household
            </Text>
          </List.Item>
        </List>

        <Box
          style={{
            marginTop: spacing.xl,
            padding: spacing.md,
            background: colors.background.secondary,
            borderRadius: '8px',
            textAlign: 'center',
          }}
        >
          <Text
            style={{
              fontSize: typography.fontSize.sm,
              color: colors.text.secondary,
              fontStyle: 'italic',
            }}
          >
            This project was made possible with generous support from{' '}
            <Text
              component="a"
              href="https://arnoldventures.org"
              target="_blank"
              rel="noopener noreferrer"
              style={{
                color: colors.primary[500],
                textDecoration: 'none',
              }}
            >
              Arnold Ventures
            </Text>
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
