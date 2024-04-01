export const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  // Correctly typed options for TypeScript
  const options: Intl.DateTimeFormatOptions = {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
    timeZone: "UTC",
  };

  // Using toLocaleString to combine date and time formatting in one go
  let formattedDate = date.toLocaleString("en-US", options);

  // Custom rearrangement to DD-MM-YYYY TIME AM/PM format
  // Extract parts using regex from the formatted string
  const matches = formattedDate.match(
    /(\d{2})\/(\d{2})\/(\d{4}), (\d{2}:\d{2}:\d{2}) (AM|PM)/,
  );
  if (matches) {
    // Reorder and format the date string as per requirement
    formattedDate = `${matches[2]}-${matches[1]}-${matches[3]} ${matches[4]} ${matches[5]}`;
  }

  return formattedDate;
};
