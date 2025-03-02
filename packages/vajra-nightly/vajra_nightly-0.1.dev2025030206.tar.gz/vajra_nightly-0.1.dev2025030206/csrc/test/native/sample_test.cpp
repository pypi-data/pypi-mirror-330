#include <gtest/gtest.h>
#include <glog/logging.h>

// Sample test suite
TEST(SampleTest, BasicAssertions) {
    // Basic assertions
    EXPECT_TRUE(true);
    EXPECT_EQ(2 + 2, 4);
    
    // Demonstrate string comparison
    std::string test_string = "hello";
    EXPECT_EQ(test_string, "hello");
    
    // Demonstrate floating point comparison
    EXPECT_NEAR(3.14159, 3.14, 0.01);
}

// Example of testing exceptions
TEST(SampleTest, ExceptionTest) {
    EXPECT_THROW({
        throw std::runtime_error("test exception");
    }, std::runtime_error);
}
