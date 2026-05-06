package com.chimera.demo;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.chimera.demo.model.Document;
import com.chimera.demo.model.User;
import com.chimera.demo.repository.DocumentRepository;
import com.chimera.demo.repository.UserRepository;

import net.datafaker.Faker;

@Configuration
public class DataSeederConfig {

    @Bean
    CommandLineRunner initMassiveDatabase(UserRepository userRepository, DocumentRepository documentRepository) {
        return args -> {
            if (userRepository.count() > 0) {
                System.out.println("Banco H2 já populado. Pulando Seeder...");
                return;
            }

            System.out.println("Iniciando geração de dados sintéticos em MASSA...");
            Faker faker = new Faker(new Locale("pt", "BR"));

            // Parâmetros de escala
            int totalUsers = 500; 
            int batchSize = 100;  

            List<User> userBatch = new ArrayList<>();
            List<Document> documentBatch = new ArrayList<>();

            for (int i = 1; i <= totalUsers; i++) {
                User user = new User();
                user.setUsername(faker.name().fullName());
                     user.setRole(i <= 5 ? "ADMIN" : "USER"); // Apenas os 5 primeiros são admins

                userBatch.add(user);

                // Quando atingir o tamanho do lote ou o final do loop, executa o salvamento
                if (i % batchSize == 0 || i == totalUsers) {
                    
                    // 1. Salva o lote de usuários (O JPA retorna a lista com os IDs gerados)
                    List<User> savedUsers = userRepository.saveAll(userBatch);
                    
                    // 2. Gera documentos vinculados aos usuários recém-criados
                    for (User savedUser : savedUsers) {
                        int numDocs = faker.number().numberBetween(2, 7); // 2 a 6 docs por usuário
                        for (int j = 0; j < numDocs; j++) {
                            Document doc = new Document();
                            doc.setTitle(faker.book().title());
                            doc.setContent(faker.lorem().paragraph(2));
                            doc.setOwnerId(savedUser.getId());
                            documentBatch.add(doc);
                        }
                    }
                    
                    // 3. Salva o lote de documentos
                    documentRepository.saveAll(documentBatch);
                    
                    // 4. Limpa as listas para liberar memória RAM e evitar OutOfMemoryError
                    userBatch.clear();
                    documentBatch.clear();
                    
                    System.out.println("Lote processado... Total de usuários até agora: " + i);
                }
            }
            
            System.out.println("✅ Geração massiva concluída! Banco de dados pronto para testes ofensivos.");
        };
    }
}