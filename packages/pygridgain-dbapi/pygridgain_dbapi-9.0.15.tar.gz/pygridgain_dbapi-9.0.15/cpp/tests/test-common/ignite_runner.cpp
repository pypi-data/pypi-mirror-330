/*
 *  Copyright (C) GridGain Systems. All Rights Reserved.
 *  _________        _____ __________________        _____
 *  __  ____/___________(_)______  /__  ____/______ ____(_)_______
 *  _  / __  __  ___/__  / _  __  / _  / __  _  __ `/__  / __  __ \
 *  / /_/ /  _  /    _  /  / /_/ /  / /_/ /  / /_/ / _  /  _  / / /
 *  \____/   /_/     /_/   \_,__/   \____/   \__,_/  /_/   /_/ /_/
 */

#include "ignite_runner.h"
#include "test_utils.h"

#include "ignite/common/detail/config.h"

#include <filesystem>
#include <iostream>
#include <sstream>
#include <stdexcept>

namespace {

/**
 * System shell command string.
 */
constexpr std::string_view SYSTEM_SHELL = IGNITE_SWITCH_WIN_OTHER("cmd.exe", "/bin/sh");
constexpr std::string_view SYSTEM_SHELL_ARG_0 = IGNITE_SWITCH_WIN_OTHER("/c ", "-c");
constexpr std::string_view GRADLEW_SCRIPT = IGNITE_SWITCH_WIN_OTHER("gradlew.bat", "./gradlew");

const std::string ADDITIONAL_JVM_OPTIONS_ENV = "CPP_ADDITIONAL_JVM_OPTIONS";

} // anonymous namespace

namespace ignite {

void ignite_runner::start() {
    std::string home = resolve_ignite_home();
    if (home.empty())
        throw std::runtime_error("Can not resolve Ignite home directory. Try setting IGNITE_HOME explicitly");

    std::vector<std::string> args;
    args.emplace_back(SYSTEM_SHELL_ARG_0);

    std::string command{GRADLEW_SCRIPT};
    command += " :ignite-runner:runnerPlatformTest"
               " --no-daemon"
               " -x compileJava"
               " -x compileTestFixturesJava"
               " -x compileIntegrationTestJava"
               " -x compileTestJava";

    auto additional_opts = detail::get_env(ADDITIONAL_JVM_OPTIONS_ENV);
    if (additional_opts) {
        command += " " + *additional_opts;
    }

    args.emplace_back(command);

    m_process = CmdProcess::make(std::string(SYSTEM_SHELL), args, home);
    if (!m_process->start()) {
        m_process.reset();

        std::stringstream argsStr;
        for (auto &arg : args)
            argsStr << arg << " ";

        throw std::runtime_error("Failed to invoke Ignite command: '" + argsStr.str() + "'");
    }
}

void ignite_runner::stop() {
    if (m_process)
        m_process->kill();
}

void ignite_runner::join(std::chrono::milliseconds timeout) {
    if (m_process)
        m_process->join(timeout);
}

} // namespace ignite