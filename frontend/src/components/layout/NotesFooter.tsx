/**
 * Notes footer with technical notes and documentation links.
 */

import { Accordion, Text, Stack, Anchor } from '@mantine/core';
import { colors, spacing, typography } from '@/designTokens';

export function NotesFooter() {
  return (
    <Accordion
      variant="contained"
      styles={{
        root: { maxWidth: '900px', margin: `${spacing.md} auto`, width: '100%' },
        label: { fontSize: typography.fontSize.sm, fontWeight: typography.fontWeight.medium },
        content: { padding: spacing.md },
      }}
    >
      <Accordion.Item value="notes">
        <Accordion.Control>Notes</Accordion.Control>
        <Accordion.Panel>
          <Stack gap={spacing.sm}>
            <Text size="sm" c={colors.text.secondary}>
              The calculator uses tax year 2026 for all calculations excluding budget window estimates.
            </Text>
            <Text size="sm" c={colors.text.secondary}>
              All computations are performed in $500 increments.
            </Text>
            <Text size="sm" c={colors.text.secondary}>
              We limit the computation to the federal budgetary impact due to: (1) state tax changes
              are secondary effects; (2) behavioral responses at the state level are harder to model;
              (3) the focus is on federal SALT/AMT policy.
            </Text>
            <Text size="sm" c={colors.text.secondary}>
              <Anchor
                href="https://docs.google.com/document/d/1ATmkzrq8e5TS-p4JrIgyXovqFdHEHvnPtqpUC0z8GW0/preview"
                target="_blank"
                rel="noopener noreferrer"
                style={{ color: colors.primary[500] }}
              >
                How we model SALT
              </Anchor>
              {' | '}
              <Anchor
                href="https://docs.google.com/document/d/1uAwllrnbS7Labq7LvxSEjUdZESv0H5roDhmknldqIDA/preview"
                target="_blank"
                rel="noopener noreferrer"
                style={{ color: colors.primary[500] }}
              >
                How we model AMT
              </Anchor>
            </Text>
          </Stack>
        </Accordion.Panel>
      </Accordion.Item>
    </Accordion>
  );
}
