export const emailPattern = {
  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
  message: "Invalid email address",
}

export const namePattern = {
  value: /^[A-Za-z\s\u00C0-\u017F]{1,30}$/,
  message: "Invalid name",
}

export const passwordRules = (isRequired = true) => {
  const rules: any = {
    minLength: {
      value: 8,
      message: "Password must be at least 8 characters",
    },
  }

  if (isRequired) {
    rules.required = "Password is required"
  }

  return rules
}

export const confirmPasswordRules = (
  getValues: () => any,
  isRequired = true,
) => {
  const rules: any = {
    validate: (value: string) => {
      const password = getValues().password || getValues().new_password
      return value === password ? true : "The passwords do not match"
    },
  }

  if (isRequired) {
    rules.required = "Password confirmation is required";
  }

  return rules;
}

export const convertDateToHumanReadable = ( apiDate: string ) => {
  const date = new Date(apiDate);

  // Example of formatting to a nice human-readable format
  const readableDate = date.toLocaleString('en-US', {
    weekday: 'long', // "Monday"
    year: 'numeric', // "2024"
    month: 'long', // "May"
    day: 'numeric', // "12"
    hour: 'numeric', // "7"
    minute: 'numeric', // "18"
    second: 'numeric', // "11"
  });

  return readableDate
}
