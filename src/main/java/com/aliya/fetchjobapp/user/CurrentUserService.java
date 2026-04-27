package com.aliya.fetchjobapp.user;

import com.aliya.fetchjobapp.common.ApiException;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

@Service
public class CurrentUserService {

    private final AppUserRepository userRepository;

    public CurrentUserService(AppUserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public AppUser requireUser() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || auth.getName() == null || "anonymousUser".equals(auth.getName())) {
            throw new ApiException("Authentication required");
        }

        return userRepository.findByEmailIgnoreCase(auth.getName())
                .orElseThrow(() -> new ApiException("User not found"));
    }
}
