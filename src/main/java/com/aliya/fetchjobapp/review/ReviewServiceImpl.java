package com.aliya.fetchjobapp.review;


import com.aliya.fetchjobapp.company.Company;
import com.aliya.fetchjobapp.company.CompanyRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class ReviewServiceImpl implements ReviewService{

    private final ReviewRepository reviewRepository;
    private final CompanyRepository companyRepository;

    public ReviewServiceImpl(ReviewRepository reviewRepository,
                             CompanyRepository companyRepository) {
        this.reviewRepository = reviewRepository;
        this.companyRepository = companyRepository;
    }

    @Override
    public List<ReviewDTO> findAllByCompanyId(Long companyId) {
        return reviewRepository.findByCompanyId(companyId)
                .stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    @Override
    public ReviewDTO findById(Long companyId, Long reviewId) {
        return reviewRepository.findById(reviewId)
                .filter(r -> r.getCompany() != null && r.getCompany().getId().equals(companyId))
                .map(this::toDTO)
                .orElse(null);
    }

    @Override
    public ReviewDTO save(Long companyId, ReviewDTO reviewDTO) {
        Optional<Company> optionalCompany = companyRepository.findById(companyId);
        if (optionalCompany.isEmpty()) {
            return null;
        }
        Review review = toEntity(reviewDTO);
        review.setCompany(optionalCompany.get());
        Review saved = reviewRepository.save(review);
        return toDTO(saved);
    }

    @Override
    public ReviewDTO update(Long companyId, Long reviewId, ReviewDTO reviewDTO) {
        Optional<Review> optionalReview = reviewRepository.findById(reviewId);
        if (optionalReview.isEmpty()) {
            return null;
        }
        Review review = optionalReview.get();
        if (review.getCompany() == null || !review.getCompany().getId().equals(companyId)) {
            return null;
        }
        review.setTitle(reviewDTO.getTitle());
        review.setDescription(reviewDTO.getDescription());
        review.setRating(reviewDTO.getRating());
        Review updated = reviewRepository.save(review);
        return toDTO(updated);
    }

    @Override
    public boolean deleteById(Long companyId, Long reviewId) {
        Optional<Review> optionalReview = reviewRepository.findById(reviewId);
        if (optionalReview.isEmpty()) {
            return false;
        }
        Review review = optionalReview.get();
        if (review.getCompany() == null || !review.getCompany().getId().equals(companyId)) {
            return false;
        }
        reviewRepository.deleteById(reviewId);
        return true;
    }

    private ReviewDTO toDTO(Review review) {
        Long companyId = review.getCompany() != null ? review.getCompany().getId() : null;
        return new ReviewDTO(
                review.getId(),
                review.getTitle(),
                review.getDescription(),
                review.getRating(),
                companyId
        );
    }

    private Review toEntity(ReviewDTO dto) {
        Review review = new Review();
        review.setTitle(dto.getTitle());
        review.setDescription(dto.getDescription());
        review.setRating(dto.getRating());
        return review;
    }

}
