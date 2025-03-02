################################
Vajra C++ Style Guide
################################

Introduction
==================
This style guide outlines the coding conventions and best practices for writing C++ code within the Vajra project. Adhering to these guidelines is crucial for ensuring code consistency, readability, maintainability, and collaboration among developers.

Key Goals
==================
- **Readability**: Code should be easy to understand and follow by any developer
- **Consistency**: Uniformity in style across the project reduces cognitive load and improves predictability
- **Maintainability**: Well-structured and clearly written code is easier to modify, debug, and extend over time
- **Collaboration**: Shared style guidelines facilitate seamless teamwork and code integration

Core Principles
==================
- **Clarity over Brevity**: Favor code that is explicit and easy to understand
- **Consistency is Key**: Apply style rules consistently throughout the project
- **Modern C++ Practices**: Embrace modern C++ features (C++11 and later)
- **Purposeful Naming**: Choose clear and accurate names
- **Pragmatism**: Balance ideal style with practical efficiency

Naming Conventions
==================

General Casing
------------------
- **PascalCase**: Used for class names, struct names, and enum names
    - Examples: ``LlamaMLP``, ``ColumnParallelLinear``, ``ActivationFunction``
- **camelCase**: Used for variable names, function names, and method names
    - Examples: ``inputTensor``, ``calculateLoss``, ``forwardPass``
- **lowercase**: Used for namespaces
    - Examples: ``vajra``, ``utils``
- **UPPER_SNAKE_CASE**: Used for constants and macros
    - Examples: ``MAX_ITERATIONS``, ``DEFAULT_LEARNING_RATE``

Variable Naming
------------------
- **Descriptive Names**: Choose names that clearly indicate the variable's purpose and meaning
- **Prefixes and Suffixes**:
    - ``m_``: Prefix for member variables of a class
        - Example: ``m_inputLayer``, ``m_spWeightMatrix``
    - ``sp``: Prefix for std::shared_ptr variables
        - Example: ``m_spGateUpProj``, ``m_spAttentionWrapper``
    - ``vsp``: Prefix for vectors of shared pointers
        - Example: ``m_vspLayers``, ``vspDecoders``
    - ``n``: Prefix for integer variables representing counts or sizes
        - Example: ``nTokens``, ``nLayers``, ``nEmbeddingSize``
    - ``v``: Prefix for variables that are std::vector
        - Example: ``vLayers``, ``vKvCaches``, ``vHiddenStates``

Function and Method Naming
------------------------------
- **Verb-Noun Style**: Function names should be verbs or verb phrases
    - Examples: ``Forward``, ``CalculateLoss``, ``InitializeWeights``
- **Forward Convention**: Use ``Forward`` as the primary method name for forward pass computation
- **Class/Struct Names**: Use nouns or noun phrases
    - Examples: ``LlamaDecoderLayer``, ``RMSNorm``, ``VocabParallelEmbedding``

Code Organization and Layout
==============================

File Structure
------------------
Each source file should follow this general layout:

1. Include statements
2. Namespace declarations
3. Class/function implementations
4. Major sections separated by comment lines

.. code-block:: cpp

    #include "Llama.h"
    #include "ops.h"
    //==============================================================================
    using namespace vajra;
    //==============================================================================
    // Class implementations follow...
    //==============================================================================

Constructor Implementation
----------------------------
- Initialize member variables using initialization lists
- Place each member initialization on a new line
- Perform assertions to validate required dependencies

.. code-block:: cpp

    LlamaMLP::LlamaMLP(
        const std::shared_ptr<ColumnParallelLinear> spGateUpProj,
        const std::shared_ptr<RowParallelLinear> spDownProj)
        : m_spGateUpProj(spGateUpProj),
          m_spDownProj(spDownProj)
    {
        ASSERT(m_spGateUpProj);
        ASSERT(m_spDownProj);
    }

Member Function Implementation
--------------------------------
- Mark member functions as ``const`` when they don't modify object state
- Include parameter direction annotations
- Use meaningful variable names

.. code-block:: cpp

    torch::Tensor LlamaAttention::Forward(
        const torch::Tensor& positions,    /*[in]*/
        const torch::Tensor& hiddenStates, /*[in]*/
        torch::Tensor& kvCache            /*[inout]*/
    ) const
    {
        // Implementation...
    }

C++ Best Practices
====================

Const Correctness
------------------
- Mark member functions as ``const`` when they don't modify object state
- Use ``const`` parameters for function arguments that shouldn't be modified
- Use ``const`` references to avoid copying and prevent modification
- Apply ``const`` to member variables that should not change after initialization

.. code-block:: cpp

    class Example {
    public:
        int getValue() const { return m_value; }  // const member function
        void process(const std::string& input);   // const reference parameter
    private:
        const int m_constValue;                   // const member variable
    };

Exception Specifications
-------------------------
- Mark functions that don't throw exceptions with ``noexcept``
- Use ``noexcept`` for move constructors and move assignment operators
- Consider ``noexcept`` for destructors (implicitly noexcept in C++11 and later)

.. code-block:: cpp

    class SafeClass {
    public:
        SafeClass() noexcept;
        SafeClass(SafeClass&& other) noexcept;
        SafeClass& operator=(SafeClass&& other) noexcept;
        void nonThrowingOperation() noexcept;
    };

Return Value Optimization
--------------------------
- Use ``[[nodiscard]]`` for functions whose return values should not be ignored
- Apply to constructors when ignoring the result would be a logical error
- Use for error-indicating functions or functions that return resource handles

.. code-block:: cpp

    [[nodiscard]] bool validate() const;
    [[nodiscard]] std::unique_ptr<Resource> createResource();

Parameter Documentation
========================
All function parameters must be documented with direction annotations:

- ``/*[in]*/``: Input parameter that will not be modified
- ``/*[out]*/``: Output parameter that will be modified but initial value is not used
- ``/*[inout]*/``: Parameter that will be both read and modified

Example:

.. code-block:: cpp

    void processNetwork(
        /*[in]*/ const NetworkConfig& config,
        /*[out]*/ std::vector<float>& results,
        /*[inout]*/ NetworkState& state
    );

Smart Pointers and Memory Management
========================================
- Use ``std::shared_ptr`` for resources shared across multiple components
- Follow naming convention ``sp`` prefix for shared pointer variables
- Follow naming convention ``vsp`` prefix for vectors of shared pointers
- Use member variable prefix ``m_`` in combination with smart pointer prefixes

.. code-block:: cpp

    class LlamaModel {
    private:
        std::shared_ptr<VocabParallelEmbedding> m_spEmbedTokens;
        std::vector<std::shared_ptr<LlamaDecoderLayer>> m_vspLayers;
    };

    LlamaModel::LlamaModel(
        const std::shared_ptr<VocabParallelEmbedding> spEmbedTokens,
        const std::vector<std::shared_ptr<LlamaDecoderLayer>> vspLayers)
        : m_spEmbedTokens(spEmbedTokens),
          m_vspLayers(vspLayers)
    {
        ASSERT(m_vspLayers.size() > 0);
    }

Assertions and Validation
===========================
- Use ``ASSERT`` macro for validating preconditions and invariants
- Always validate smart pointer members in constructors
- Check container sizes and other critical assumptions
- Place assertions immediately after initialization in constructors

.. code-block:: cpp

    class LlamaDecoderLayer {
    public:
        LlamaDecoderLayer(
            const std::shared_ptr<LlamaAttention> spSelfAttn,
            const std::shared_ptr<LlamaMLP> spMlp)
            : m_spSelfAttn(spSelfAttn),
              m_spMlp(spMlp)
        {
            ASSERT(m_spSelfAttn);  // Validate required dependencies
            ASSERT(m_spMlp);
        }
    };

Input and Output Checks & Error Handling
=========================================

Input Validation
------------------
- Validate function inputs, especially from external sources
- Use assertions to check preconditions during development
- Implement proper input validation for production code

Error Handling
------------------
- Use exceptions for exceptional conditions
- Use logging macros defined in logging.h
- Do not use std::cout
- Use fmt for log formatting

Modern C++ Features
=====================
- Use ``auto`` for complex types or when type is clear from context
- Prefer range-based for loops when iterating over containers
- Use structured bindings for multiple return values
- Leverage ``constexpr`` for compile-time evaluation
- Use ``enum class`` instead of plain enums
- Utilize ``std::array`` for fixed-size arrays

.. code-block:: cpp

    enum class ActivationType {
        ReLU,
        Sigmoid,
        Tanh
    };

    constexpr size_t calculateSize() {
        return 2 * sizeof(float);
    }

    void processData() {
        std::array<float, calculateSize()> buffer;
        for (const auto& value : buffer) {
            // Process value
        }
    }

Comments
==================
- Use ``//`` for single-line comments
- Use ``/* ... */`` for block comments
- Use ``/*[in]*/, /*[out]*/, /*[inout]*/`` for parameter documentation
- Use ``// TODO(Developer Name): Description`` for future tasks
- Use ``//==============================================================================`` for major section separation

.. code-block:: cpp

    //==============================================================================
    // Major section separator
    //==============================================================================
    
    /* Block comment for 
       multiple lines */
       
    // Single line comment
    
    // TODO(John): Implement error handling
    void process(
        /*[in]*/ const Data& input,
        /*[out]*/ Result& output
    );