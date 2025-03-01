/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Definitions                                                      *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/


/// Verifies the dimensions of the A and B DotOp operands.
bool mlir::triton::DotOpInterface::verifyDims() {
      return getImpl()->verifyDims(getImpl(), getOperation());
  }

/// Get the source operand of the transposition.
::mlir::Value mlir::triton::TransposeOpInterface::getSrc() {
      return getImpl()->getSrc(getImpl(), getOperation());
  }

/// Get the order of the transposition.
::mlir::ArrayRef<int32_t> mlir::triton::TransposeOpInterface::getOrder() {
      return getImpl()->getOrder(getImpl(), getOperation());
  }
