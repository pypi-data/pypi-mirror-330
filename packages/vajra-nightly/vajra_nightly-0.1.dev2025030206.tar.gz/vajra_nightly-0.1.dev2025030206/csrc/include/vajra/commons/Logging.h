#pragma once

#include <fmt/format.h>
#include <fmt/ranges.h>
#include <glog/logging.h>

#include "vajra/commons/LogLevels.h"
#include "vajra/commons/StdCommon.h"
//==============================================================================
#define LOG_LEVEL LogLevel::INFO
//==============================================================================
#define LOG_DEBUG(...)                                                         \
  vajra::Logger::log(vajra::LogLevel::DEBUG, __FILE__, __LINE__, __VA_ARGS__)
#define LOG_INFO(...)                                                          \
  vajra::Logger::log(vajra::LogLevel::INFO, __FILE__, __LINE__, __VA_ARGS__)
#define LOG_WARNING(...)                                                       \
  vajra::Logger::log(vajra::LogLevel::WARNING, __FILE__, __LINE__, __VA_ARGS__)
#define LOG_ERROR(...)                                                         \
  vajra::Logger::log(vajra::LogLevel::ERROR, __FILE__, __LINE__, __VA_ARGS__)
#define LOG_CRITICAL(...)                                                      \
  vajra::Logger::log(vajra::LogLevel::CRITICAL, __FILE__, __LINE__, __VA_ARGS__)
//==============================================================================
#define EXCEPTION_FORMAT "Message: {}\nFile: {}\nLine number: {}\n"
//==============================================================================
#define ASSERT(x)                                                              \
  if (!(x))                                                                    \
  {                                                                            \
    LOG_CRITICAL("ASSERTION FAILED: %s", #x);                                  \
    exit(1);                                                                   \
  }
//==============================================================================
#define TRACE_CRITICAL_AND_EXIT(fmt, ...)                                      \
  LOG_CRITICAL(fmt, ##__VA_ARGS__);                                            \
  exit(1);
//==============================================================================
#define ASSERT_VALID_ARGUMENTS(x, message)                                     \
  if (!(x))                                                                    \
  {                                                                            \
    LOG_CRITICAL("ASSERTION FAILED: %s, Message: %s", #x, message);            \
    throw std::invalid_argument(                                               \
        fmt::format(EXCEPTION_FORMAT, message, __FILE__, __LINE__));           \
  }
//==============================================================================
#define ASSERT_VALID_RUNTIME(x, message)                                       \
  if (!(x))                                                                    \
  {                                                                            \
    LOG_CRITICAL("ASSERTION FAILED: %s, Message: %s", #x, message);            \
    throw std::runtime_error(                                                  \
        fmt::format(EXCEPTION_FORMAT, message, __FILE__, __LINE__));           \
  }
//==============================================================================

namespace vajra
{
class Logger
{
public:
  template <typename... Args>
  static inline void
  log(LogLevel severity,
      const std::string file,
      int line,
      const std::string format,
      const Args&... args)
  {
    if (severity < LOG_LEVEL)
    {
      return;
    }

    std::string message = fmt::format(format, args...);
    switch (severity)
    {
    case LogLevel::DEBUG:
    case LogLevel::INFO:
      LOG(INFO) << "[" << file << ":" << line << "] " << message;
      break;
    case LogLevel::WARNING:
      LOG(WARNING) << "[" << file << ":" << line << "] " << message;
      break;
    case LogLevel::ERROR:
      LOG(ERROR) << "[" << file << ":" << line << "] " << message;
      break;
    case LogLevel::CRITICAL:
      LOG(ERROR) << "[" << file << ":" << line << "] " << message;
      break;
    default:
      LOG(INFO) << "[" << file << ":" << line << "] " << message;
      break;
    }
  }
};
} // namespace vajra
//==============================================================================
