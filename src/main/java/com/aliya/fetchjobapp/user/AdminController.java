package com.aliya.fetchjobapp.user;

import com.aliya.fetchjobapp.application.JobApplicationRepository;
import com.aliya.fetchjobapp.company.CompanyRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/api/admin")
public class AdminController {

    private final AppUserRepository userRepository;
    private final CompanyRepository companyRepository;
    private final JobRepository jobRepository;
    private final JobApplicationRepository applicationRepository;

    public AdminController(
            AppUserRepository userRepository,
            CompanyRepository companyRepository,
            JobRepository jobRepository,
            JobApplicationRepository applicationRepository
    ) {
        this.userRepository = userRepository;
        this.companyRepository = companyRepository;
        this.jobRepository = jobRepository;
        this.applicationRepository = applicationRepository;
    }

    @GetMapping("/overview")
    public Map<String, Object> overview() {
        return Map.of(
                "users", userRepository.count(),
                "companies", companyRepository.count(),
                "jobs", jobRepository.count(),
                "applications", applicationRepository.count()
        );
    }
}
