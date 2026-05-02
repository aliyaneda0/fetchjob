package com.aliya.fetchjobapp.job;

import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/jobs")
public class JobController {


    private final JobServiceImpl jobServiceImpl;

    public JobController(JobServiceImpl jobServiceImpl){
        this.jobServiceImpl = jobServiceImpl;
    }


    ArrayList<Job> jobs = new ArrayList<>();

    @GetMapping
    public List<Job> findAll(){

        return jobs;
    }

    @GetMapping("/{id}")
    public JobDTO getJobById(@PathVariable Long id){

        return jobServiceImpl.getJobById(id);
    }

    @PostMapping
    public void createJob(@Valid @RequestBody JobDTO jobDTO){
         jobServiceImpl.createJob(jobDTO);
    }
}
