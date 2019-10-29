const api = {
  /**
   * Validates token.
   * @param token Token.
   * @returns {Promise<{username: string}>} Promise which resolves to the user.
   */
  validateToken: async (token) => {
    return { username: 'xxx' };
  },
  /**
   * Checks whether the given username is taken.
   * @param username Username to check.
   * @returns {Promise<boolean>} Promise which resolves to true if the username is not taken.
   */
  checkUsernameAvailability: async (username) => {
    return true;
  },
  /**
   * Registers a new user.
   * @param username Username.
   * @param password Password as raw output.
   * @param confirmPassword Confirm password as raw output.
   * @param height Height of password grid.
   * @param width Width of password grid.
   * @returns {Promise<void>} Promose which resolves if registration was successful, else throws error.
   */
  register: async (username, password, confirmPassword, height, width) => {

  },

  login: async (username, password, height, width) => {

  },

  logout: async () => {

  }
};

export default api;
