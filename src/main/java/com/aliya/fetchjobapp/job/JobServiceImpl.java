package com.aliya.fetchjobapp.job;


import com.aliya.fetchjobapp.exception.ResourceNotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class JobServiceImpl implements JobService {

    private final JobRepository jobRepository;

    // constructor injection — never use @Autowired on a field
    public JobServiceImpl(JobRepository jobRepository) {
        this.jobRepository = jobRepository;
    }

    @Override
    @Transactional
    public JobDTO createJob(JobDTO jobDTO) {
        Job job = toEntity(jobDTO);
        Job saved = jobRepository.save(job);
        return toDTO(saved);
    }

    @Override
    public List<JobDTO> getAllJobs() {
        return jobRepository.findAll()
                .stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    @Override
    public JobDTO getJobById(Long id) {
        Job job = jobRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException(
                        "Job not found with id: " + id));
        return toDTO(job);
    }

    @Override
    @Transactional
    public JobDTO updateJob(Long id, JobDTO jobDTO) {
        Job job = jobRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException(
                        "Job not found with id: " + id));

        // update only the fields that came in
        job.setTitle(jobDTO.getTitle());
        job.setDescription(jobDTO.getDescription());
        job.setMinSalary(jobDTO.getMinSalary());
        job.setMaxSalary(jobDTO.getMaxSalary());
        job.setLocation(jobDTO.getLocation());

        if (jobDTO.getStatus() != null) {
            job.setStatus(jobDTO.getStatus());
        }

        // no need to call save() — JPA tracks the entity
        // and flushes changes on transaction commit (@Transactional)
        return toDTO(job);
    }

    @Override
    @Transactional
    public void deleteJob(Long id) {
        if (!jobRepository.existsById(id)) {
            throw new ResourceNotFoundException("Job not found with id: " + id);
        }
        jobRepository.deleteById(id);
    }

    // ── private mappers ──────────────────────────────────────

    private JobDTO toDTO(Job job) {
        JobDTO dto = new JobDTO();
        dto.setId(job.getId());
        dto.setTitle(job.getTitle());
        dto.setDescription(job.getDescription());
        dto.setMinSalary(job.getMinSalary());
        dto.setMaxSalary(job.getMaxSalary());
        dto.setLocation(job.getLocation());
        dto.setStatus(job.getStatus());
        dto.setCreatedAt(job.getCreatedAt());
        return dto;
    }

    private Job toEntity(JobDTO dto) {
        Job job = new Job();
        job.setTitle(dto.getTitle());
        job.setDescription(dto.getDescription());
        job.setMinSalary(dto.getMinSalary());
        job.setMaxSalary(dto.getMaxSalary());
        job.setLocation(dto.getLocation());
        job.setStatus(dto.getStatus() != null ? dto.getStatus() : JobStatus.DRAFT);
        return job;
    }
}
