# Ray

## Overview

Ray is an open-source unified framework for scaling Python applications and machine learning workloads. It provides a simple, universal API for building distributed applications, with a focus on making distributed computing accessible to ML practitioners without requiring deep systems expertise.

Developed at UC Berkeley's RISELab and now maintained by Anyscale, Ray has become one of the most popular frameworks for distributed machine learning, serving companies like OpenAI, Uber, Amazon, and Alibaba.

## Core Concepts

### Architecture

Ray consists of several key components:

**Application Layer**:
- **Tasks**: Stateless functions that run remotely
- **Actors**: Stateful classes that maintain state across method calls
- **Objects**: Immutable values stored in distributed shared memory

**System Layer**:
- **Ray Core**: The foundational distributed runtime
- **Object Store**: Distributed shared-memory object store using Apache Arrow
- **Scheduler**: Distributed task scheduler with locality-aware scheduling
- **Global Control Store (GCS)**: Centralized metadata store

### Key Features

**1. Simple API**
```python
import ray

# Initialize Ray
ray.init()

# Parallelize a function
@ray.remote
def expensive_function(x):
    return x * x

# Execute in parallel
futures = [expensive_function.remote(i) for i in range(100)]
results = ray.get(futures)
```

**2. Distributed Data**
- Zero-copy shared memory for efficient data sharing
- Automatic data transfer between nodes
- Support for large objects (>100GB)

**3. Fault Tolerance**
- Automatic retry of failed tasks
- Actor reconstruction
- Lineage-based recovery

**4. Dynamic Resource Management**
- Automatic scaling based on demand
- Resource-aware scheduling
- Support for heterogeneous hardware (CPUs, GPUs, TPUs)

## Ray Libraries

Ray provides high-level libraries for common ML workloads:

### Ray Train
Distributed training for deep learning models.

**Features**:
- Integration with PyTorch, TensorFlow, Hugging Face
- Fault-tolerant distributed training
- Hyperparameter tuning integration
- Multi-node, multi-GPU training

**Use case**: Train large language models across multiple GPUs/nodes

### Ray Serve
Scalable model serving and inference.

**Features**:
- Model deployment with minimal code changes
- Autoscaling based on requests
- Model composition and ensemble serving
- A/B testing and canary deployments

**Use case**: Deploy ML models at scale with automatic load balancing

### Ray Data
Scalable data processing for ML.

**Features**:
- Distributed data loading and preprocessing
- Integration with ML training libraries
- Streaming execution for large datasets
- GPU-accelerated operations

**Use case**: ETL pipelines for ML training data

### Ray Tune
Distributed hyperparameter tuning.

**Features**:
- Support for various tuning algorithms (Grid Search, Bayesian Optimization, HyperBand, PBT)
- Early stopping strategies
- Integration with popular ML frameworks
- Distributed execution across clusters

**Use case**: Hyperparameter optimization for deep learning models

### Ray RLlib
Scalable reinforcement learning.

**Features**:
- Production-ready RL algorithms
- Distributed training for RL
- Multi-agent support
- Custom environment integration

**Use case**: Training RL agents for robotics, gaming, recommendation systems

## When to Use Ray

**Ray is excellent for**:

✅ **Distributed ML workloads**: Training large models, hyperparameter tuning, model serving
✅ **Data-parallel tasks**: Processing large datasets in parallel
✅ **Python-first workflows**: Teams already using Python want to scale
✅ **Dynamic workloads**: Task graphs that change during execution
✅ **Stateful computations**: When you need actors with persistent state
✅ **ML pipelines**: End-to-end ML workflows (data → training → serving)

**Consider alternatives when**:

⚠️ **Pure data processing**: Spark might be more mature for ETL-heavy workloads
⚠️ **Non-Python ecosystems**: If your stack isn't Python-centric
⚠️ **Simple batch jobs**: Kubernetes Jobs might be simpler
⚠️ **Streaming-first**: Flink or Spark Streaming for low-latency stream processing

## Ray vs. Other Frameworks

### Ray vs. Kubernetes

**They're complementary, not alternatives**:
- **Kubernetes**: Infrastructure orchestration (containers, networking, storage)
- **Ray**: Application-level distributed computing (tasks, actors, data)

**Common pattern**: Run Ray ON Kubernetes (KubeRay operator)
- K8s manages the cluster infrastructure
- Ray manages distributed computation
- Best of both worlds: K8s reliability + Ray's ML-friendly API

### Ray vs. Spark

**Similarities**: Both are distributed computing frameworks

**Ray advantages**:
- Native Python support (Spark is JVM-based)
- Better for ML workloads (native GPU support, ML libraries)
- Stateful actors (Spark is stateless)
- Lower latency for iterative algorithms

**Spark advantages**:
- More mature ecosystem for SQL/data processing
- Better for large-scale ETL
- More enterprise tooling and support

**Rule of thumb**: Use Ray for ML, Spark for data engineering

### Ray vs. Dask

**Similarities**: Both scale Python code

**Ray advantages**:
- Actor model for stateful computation
- Better ML ecosystem (Ray Train, Serve, Tune)
- More sophisticated scheduling
- Production-ready serving (Ray Serve)

**Dask advantages**:
- Closer to pandas/NumPy API (easier migration)
- Better for NumPy/pandas workflows
- Simpler for data scientists familiar with pandas

**Rule of thumb**: Use Dask for scaling pandas/NumPy, Ray for ML pipelines

## Use Cases in LLM Serving

Ray is increasingly popular for LLM deployment:

**Distributed LLM Inference**:
- Ray Serve for deploying LLMs with tensor parallelism
- Automatic scaling based on request load
- Model ensemble (routing to different model sizes)

**Example: Serving LLaMA with Ray Serve**
```python
from ray import serve
import ray

@serve.deployment(num_replicas=2, ray_actor_options={"num_gpus": 1})
class LLMServing:
    def __init__(self):
        # Load model on GPU
        self.model = load_llama_model()

    def __call__(self, request):
        return self.model.generate(request.prompt)

serve.run(LLMServing.bind())
```

**Training LLMs**:
- Ray Train for distributed training across multiple nodes
- Integration with DeepSpeed, Megatron for large model training
- Automatic fault tolerance for long-running training jobs

**Data preprocessing**:
- Ray Data for distributed tokenization and preprocessing
- Streaming large datasets that don't fit in memory

## Deployment

### Local Development
```python
import ray
ray.init()  # Starts local Ray cluster
```

### On Kubernetes (KubeRay)
```yaml
apiVersion: ray.io/v1alpha1
kind: RayCluster
metadata:
  name: ray-cluster
spec:
  rayVersion: '2.9.0'
  headGroupSpec:
    replicas: 1
    rayStartParams: {}
  workerGroupSpecs:
  - replicas: 3
    minReplicas: 1
    maxReplicas: 10
    rayStartParams: {}
```

### Cloud Providers
- **AWS**: Ray on EC2, EKS
- **GCP**: Ray on GKE, Compute Engine
- **Azure**: Ray on AKS
- **Managed offerings**: Anyscale (fully managed Ray platform)

## Getting Started

**Installation**:
```bash
pip install ray[default]  # Core Ray
pip install ray[data]     # Add Ray Data
pip install ray[train]    # Add Ray Train
pip install ray[serve]    # Add Ray Serve
pip install ray[tune]     # Add Ray Tune
```

**Hello World**:
```python
import ray

ray.init()

@ray.remote
def hello():
    return "Hello, distributed world!"

# Execute remotely
result = ray.get(hello.remote())
print(result)
```

**Next steps**:
1. Try the [Ray Tutorial](https://docs.ray.io/en/latest/ray-core/walkthrough.html)
2. Explore [Ray Serve for model deployment](https://docs.ray.io/en/latest/serve/index.html)
3. Check [Ray Train for distributed training](https://docs.ray.io/en/latest/train/train.html)

## Related Topics

- **Kubernetes** - Ray can run on K8s for infrastructure management
- **vLLM** - Alternative LLM serving framework (can integrate with Ray Serve)
- **Distributed LLM Systems** - Ray is commonly used for distributed LLM deployment
- **Docker** - Ray applications are often containerized
- **Microservices Architecture** - Ray Serve can be part of a microservices architecture

## References

- [Official Ray Documentation](https://docs.ray.io/)
- [Ray GitHub](https://github.com/ray-project/ray)
- [Anyscale Blog](https://www.anyscale.com/blog) - Ray use cases and tutorials
- [Ray Summit Talks](https://www.youtube.com/c/TheRayProject) - Conference videos
- [Ray Paper (OSDI 2018)](https://www.usenix.org/conference/osdi18/presentation/moritz) - Original research paper
