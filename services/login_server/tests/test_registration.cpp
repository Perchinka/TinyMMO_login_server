#include "UserService.hpp"
#include "catch2/catch_test_macros.hpp"

TEST_CASE("User registration") {
  UserService service;

  SECTION("Registers a new user successfully") {
    bool result =
        service.register_user("alpha", "alpha@example.com", "secret123");
    REQUIRE(result == true);
  }

  SECTION("Fails to register a user with an existing email") {
    service.register_user("alpha", "alpha@example.com", "secret123");
    bool result =
        service.register_user("alpha", "alpha@example.com", "secret123");
    REQUIRE(result == false);
  }

  SECTION("Fails to register a user with an existing username") {
    service.register_user("alpha", "alpha@example.com", "secret123");
    bool result =
        service.register_user("alpha", "different@example.com", "secret123");
    REQUIRE(result == false);
  }
}
