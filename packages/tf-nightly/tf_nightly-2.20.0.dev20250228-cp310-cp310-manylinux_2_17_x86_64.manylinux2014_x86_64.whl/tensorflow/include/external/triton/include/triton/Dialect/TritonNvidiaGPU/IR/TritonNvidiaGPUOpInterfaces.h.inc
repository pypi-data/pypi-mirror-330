/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Declarations                                                     *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace triton {
namespace nvidia_gpu {
class MMAv5OpInterface;
namespace detail {
struct MMAv5OpInterfaceInterfaceTraits {
  struct Concept {
    /// The methods defined by the interface.
    ::mlir::Value (*useAccumulator)(const Concept *impl, ::mlir::Operation *);
    void (*setUseAccumulator)(const Concept *impl, ::mlir::Operation *, ::mlir::Value);
    void (*setBarrier)(const Concept *impl, ::mlir::Operation *, ::mlir::Value);
    ::mlir::Value (*getAccumulator)(const Concept *impl, ::mlir::Operation *);
    void (*setAccumulator)(const Concept *impl, ::mlir::Operation *, ::mlir::Value);
    ::mlir::Value (*getPredicate)(const Concept *impl, ::mlir::Operation *);
    void (*setPredicate)(const Concept *impl, ::mlir::Operation *, ::mlir::Value);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = ::mlir::triton::nvidia_gpu::MMAv5OpInterface;
    Model() : Concept{useAccumulator, setUseAccumulator, setBarrier, getAccumulator, setAccumulator, getPredicate, setPredicate} {}

    static inline ::mlir::Value useAccumulator(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline void setUseAccumulator(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Value flag);
    static inline void setBarrier(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Value barrier);
    static inline ::mlir::Value getAccumulator(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline void setAccumulator(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Value accum);
    static inline ::mlir::Value getPredicate(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline void setPredicate(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Value pred);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::triton::nvidia_gpu::MMAv5OpInterface;
    FallbackModel() : Concept{useAccumulator, setUseAccumulator, setBarrier, getAccumulator, setAccumulator, getPredicate, setPredicate} {}

    static inline ::mlir::Value useAccumulator(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline void setUseAccumulator(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Value flag);
    static inline void setBarrier(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Value barrier);
    static inline ::mlir::Value getAccumulator(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline void setAccumulator(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Value accum);
    static inline ::mlir::Value getPredicate(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline void setPredicate(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Value pred);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    using ConcreteEntity = ConcreteOp;
  };
};
template <typename ConcreteOp>
struct MMAv5OpInterfaceTrait;

} // namespace detail
class MMAv5OpInterface : public ::mlir::OpInterface<MMAv5OpInterface, detail::MMAv5OpInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<MMAv5OpInterface, detail::MMAv5OpInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::MMAv5OpInterfaceTrait<ConcreteOp> {};

  /// Return the accumulator init flag.
  ::mlir::Value useAccumulator();

  /// Set the accumulator init flag.
  void setUseAccumulator(::mlir::Value flag);

  /// Associate a new barrier to this MMAv5 op.
  void setBarrier(::mlir::Value barrier);

  /// Return the accumulator.
  ::mlir::Value getAccumulator();

  /// Set the accumulator.
  void setAccumulator(::mlir::Value accum);

  /// Return the predicate of this op.
  ::mlir::Value getPredicate();

  /// Set the predicate of this op.
  void setPredicate(::mlir::Value pred);
};
namespace detail {
  template <typename ConcreteOp>
  struct MMAv5OpInterfaceTrait : public ::mlir::OpInterface<MMAv5OpInterface, detail::MMAv5OpInterfaceInterfaceTraits>::Trait<ConcreteOp> {
  };
}// namespace detail
} // namespace nvidia_gpu
} // namespace triton
} // namespace mlir
namespace mlir {
namespace triton {
namespace nvidia_gpu {
template<typename ConcreteOp>
::mlir::Value detail::MMAv5OpInterfaceInterfaceTraits::Model<ConcreteOp>::useAccumulator(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).useAccumulator();
}
template<typename ConcreteOp>
void detail::MMAv5OpInterfaceInterfaceTraits::Model<ConcreteOp>::setUseAccumulator(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Value flag) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).setUseAccumulator(flag);
}
template<typename ConcreteOp>
void detail::MMAv5OpInterfaceInterfaceTraits::Model<ConcreteOp>::setBarrier(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Value barrier) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).setBarrier(barrier);
}
template<typename ConcreteOp>
::mlir::Value detail::MMAv5OpInterfaceInterfaceTraits::Model<ConcreteOp>::getAccumulator(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getAccumulator();
}
template<typename ConcreteOp>
void detail::MMAv5OpInterfaceInterfaceTraits::Model<ConcreteOp>::setAccumulator(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Value accum) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).setAccumulator(accum);
}
template<typename ConcreteOp>
::mlir::Value detail::MMAv5OpInterfaceInterfaceTraits::Model<ConcreteOp>::getPredicate(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getPredicate();
}
template<typename ConcreteOp>
void detail::MMAv5OpInterfaceInterfaceTraits::Model<ConcreteOp>::setPredicate(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Value pred) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).setPredicate(pred);
}
template<typename ConcreteOp>
::mlir::Value detail::MMAv5OpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::useAccumulator(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->useAccumulator(tablegen_opaque_val);
}
template<typename ConcreteOp>
void detail::MMAv5OpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::setUseAccumulator(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Value flag) {
  return static_cast<const ConcreteOp *>(impl)->setUseAccumulator(tablegen_opaque_val, flag);
}
template<typename ConcreteOp>
void detail::MMAv5OpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::setBarrier(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Value barrier) {
  return static_cast<const ConcreteOp *>(impl)->setBarrier(tablegen_opaque_val, barrier);
}
template<typename ConcreteOp>
::mlir::Value detail::MMAv5OpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getAccumulator(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->getAccumulator(tablegen_opaque_val);
}
template<typename ConcreteOp>
void detail::MMAv5OpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::setAccumulator(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Value accum) {
  return static_cast<const ConcreteOp *>(impl)->setAccumulator(tablegen_opaque_val, accum);
}
template<typename ConcreteOp>
::mlir::Value detail::MMAv5OpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getPredicate(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->getPredicate(tablegen_opaque_val);
}
template<typename ConcreteOp>
void detail::MMAv5OpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::setPredicate(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Value pred) {
  return static_cast<const ConcreteOp *>(impl)->setPredicate(tablegen_opaque_val, pred);
}
} // namespace nvidia_gpu
} // namespace triton
} // namespace mlir
