#include "UserService.hpp"
#include "catch2/catch_test_macros.hpp"

TEST_CASE("User login") {
  UserService service;
  service.register_user("alpha", "alpha@example.com", "secret123");

  SECTION("Logs in with correct email and password") {
    bool result = service.login("alpha@example.com", "secret123");
    REQUIRE(result == true);
  }

  SECTION("Fails to log in with incorrect password") {
    bool result = service.login("alpha@example.com", "wrongpassword");
    REQUIRE(result == false);
  }

  SECTION("Fails to log in with unregistered email") {
    bool result = service.login("nonexistent@example.com", "secret123");
    REQUIRE(result == false);
  }
