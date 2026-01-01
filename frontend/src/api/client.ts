/**
 * API client for the Modal backend.
 */

import type {
  HouseholdInput,
  PolicyConfig,
  SinglePointResult,
  AxisResult,
  TwoAxesResult,
  BaselineScenario,
} from '@/types';

// Modal API base URL - update after deployment
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://policyengine--salt-amt-api.modal.run';

// Convert camelCase to snake_case for API
function toSnakeCase(obj: Record<string, unknown>): Record<string, unknown> {
  const result: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(obj)) {
    const snakeKey = key.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);
    if (value && typeof value === 'object' && !Array.isArray(value)) {
      result[snakeKey] = toSnakeCase(value as Record<string, unknown>);
    } else {
      result[snakeKey] = value;
    }
  }
  return result;
}

// Convert snake_case to camelCase for response
function toCamelCase(obj: Record<string, unknown>): Record<string, unknown> {
  const result: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(obj)) {
    const camelKey = key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
    if (value && typeof value === 'object' && !Array.isArray(value)) {
      result[camelKey] = toCamelCase(value as Record<string, unknown>);
    } else {
      result[camelKey] = value;
    }
  }
  return result;
}

async function apiCall<T>(endpoint: string, body: Record<string, unknown>): Promise<T> {
  const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(toSnakeCase(body)),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`API error: ${response.status} - ${error}`);
  }

  const data = await response.json();
  return toCamelCase(data) as T;
}

export async function calculateSinglePoint(
  household: HouseholdInput,
  baselineScenario: BaselineScenario,
  policyConfig?: PolicyConfig
): Promise<SinglePointResult> {
  return apiCall<SinglePointResult>('calculate_single', {
    household,
    baselineScenario,
    policyConfig,
  });
}

export async function calculateSaltAxis(
  household: HouseholdInput,
  baselineScenario: BaselineScenario,
  policyConfig?: PolicyConfig,
  minSalt = 0,
  maxSalt = 300000,
  count = 600
): Promise<AxisResult> {
  return apiCall<AxisResult>('calculate_salt_axis', {
    household,
    baselineScenario,
    policyConfig,
    minSalt,
    maxSalt,
    count,
  });
}

export async function calculateIncomeAxis(
  household: HouseholdInput,
  baselineScenario: BaselineScenario,
  policyConfig?: PolicyConfig,
  minIncome = 0,
  maxIncome = 1000000,
  count = 1000
): Promise<AxisResult> {
  return apiCall<AxisResult>('calculate_income_axis', {
    household,
    baselineScenario,
    policyConfig,
    minIncome,
    maxIncome,
    count,
  });
}

export async function calculateTwoAxes(
  household: HouseholdInput,
  baselineScenario: BaselineScenario,
  policyConfig?: PolicyConfig,
  options?: {
    minSalt?: number;
    maxSalt?: number;
    saltCount?: number;
    minIncome?: number;
    maxIncome?: number;
    incomeCount?: number;
  }
): Promise<TwoAxesResult> {
  return apiCall<TwoAxesResult>('calculate_two_axes', {
    household,
    baselineScenario,
    policyConfig,
    ...options,
  });
}

export async function healthCheck(): Promise<{ status: string; service: string }> {
  const response = await fetch(`${API_BASE_URL}/health`);
  return response.json();
}
