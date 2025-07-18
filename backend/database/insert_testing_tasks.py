from backend.tests.test_files_and_images.FilesEnum import file
from backend.managers.task_manager import create_task

create_task('Exploración lunar', 'Analizar cráteres lunares', '2025-02-10', '2025-02-15', file.HEIC_1311_A_JPG.value, file.STARS_CSV.value)

create_task('Estudio de galaxias', 'Comparar formas galácticas', '2025-03-05', '2025-03-20', [file.HEIC_1311_A_JPG.value, file.SOMBRERO_GALAXY_JPG.value], file.DEEP_SPACE_CSV.value)

create_task('Nebulosas planetarias', 'Catalogar nebulosas', '2025-04-01', '2025-04-30', file.SOMBRERO_GALAXY_JPG.value, [file.CRAB_NEBULA_PDF.value, file.NGC_1514_PDF.value])

create_task('Cartografía estelar', 'Actualizar mapas estelares', '2025-01-15', '2025-02-28', file.HEIC_1311_A_JPG.value, file.STARS_CSV.value)

create_task('Análisis espectral', 'Estudiar composición química de estrellas', '2025-05-10', '2025-06-10', [file.HEIC_1311_A_JPG.value, file.SOMBRERO_GALAXY_JPG.value], [file.STARS_CSV.value, file.DEEP_SPACE_CSV.value])

create_task('Monitoreo de supernovas', 'Buscar explosiones estelares', '2025-07-01', '2025-07-31', file.SOMBRERO_GALAXY_JPG.value, file.CRAB_NEBULA_PDF.value)

create_task('Clasificación estelar', 'Organizar estrellas por tipo', '2025-08-12', '2025-09-12', file.HEIC_1311_A_JPG.value, file.NGC_1514_PDF.value)

create_task('Búsqueda de exoplanetas', 'Identificar planetas en zona habitable', '2025-09-01', '2025-12-31', [file.HEIC_1311_A_JPG.value, file.SOMBRERO_GALAXY_JPG.value], file.DEEP_SPACE_CSV.value)

create_task('Estudio de cúmulos', 'Analizar cúmulos globulares', '2025-10-15', '2025-11-15', file.SOMBRERO_GALAXY_JPG.value, [file.STARS_CSV.value, file.CRAB_NEBULA_PDF.value])

create_task('Radioastronomía', 'Mapear fuentes de radio', '2025-11-01', '2026-01-31', file.HEIC_1311_A_JPG.value, file.NGC_1514_PDF.value)

create_task('Fotometría estelar', 'Medir brillo de estrellas variables', '2026-01-10', '2026-02-28', [file.HEIC_1311_A_JPG.value, file.SOMBRERO_GALAXY_JPG.value], [file.DEEP_SPACE_CSV.value, file.CRAB_NEBULA_PDF.value])

create_task('Astrobiología', 'Buscar signos de vida', '2026-03-01', '2026-05-31', file.SOMBRERO_GALAXY_JPG.value, file.STARS_CSV.value)

create_task('Cosmología', 'Estudiar estructura del universo', '2026-04-15', '2026-07-15', file.HEIC_1311_A_JPG.value, file.NGC_1514_PDF.value)

create_task('Astrometría', 'Medir posiciones estelares', '2026-06-01', '2026-08-31', [file.HEIC_1311_A_JPG.value, file.SOMBRERO_GALAXY_JPG.value], file.DEEP_SPACE_CSV.value)

create_task('Física solar', 'Analizar tormentas solares', '2026-07-10', '2026-09-10', file.SOMBRERO_GALAXY_JPG.value, [file.STARS_CSV.value, file.NGC_1514_PDF.value])

create_task('Arqueoastronomía', 'Estudiar astronomía antigua', '2026-08-01', '2026-10-31', file.HEIC_1311_A_JPG.value, file.CRAB_NEBULA_PDF.value)

create_task('Meteorítica', 'Analizar composición de meteoritos', '2026-09-15', '2026-12-15', [file.HEIC_1311_A_JPG.value, file.SOMBRERO_GALAXY_JPG.value], file.DEEP_SPACE_CSV.value)

create_task('Dinámica galáctica', 'Estudiar movimiento de galaxias', '2026-10-01', '2027-01-31', file.SOMBRERO_GALAXY_JPG.value, [file.CRAB_NEBULA_PDF.value, file.NGC_1514_PDF.value])

create_task('Óptica adaptativa', 'Probar nuevos sistemas', '2026-11-10', '2027-02-10', file.HEIC_1311_A_JPG.value, file.STARS_CSV.value)

create_task('Evolución estelar', 'Modelar ciclos de vida estelar', '2027-01-01', '2027-06-30', file.SOMBRERO_GALAXY_JPG.value, file.DEEP_SPACE_CSV.value)

create_task('Magnetosfera', 'Estudiar campos magnéticos', '2027-02-15', '2027-05-15', [file.HEIC_1311_A_JPG.value, file.SOMBRERO_GALAXY_JPG.value], [file.STARS_CSV.value, file.NGC_1514_PDF.value])

create_task('Formación planetaria', 'Observar discos protoplanetarios', '2027-03-01', '2027-09-01', file.SOMBRERO_GALAXY_JPG.value, file.CRAB_NEBULA_PDF.value)

create_task('Astroquímica', 'Analizar moléculas interestelares', '2027-04-10', '2027-10-10', file.HEIC_1311_A_JPG.value, file.DEEP_SPACE_CSV.value)

create_task('Gravitación', 'Probar teorías gravitacionales', '2027-05-01', '2027-11-30', [file.HEIC_1311_A_JPG.value, file.SOMBRERO_GALAXY_JPG.value], file.NGC_1514_PDF.value)

create_task('Púlsares', 'Monitorear estrellas de neutrones', '2027-06-15', '2027-12-15', file.SOMBRERO_GALAXY_JPG.value, [file.STARS_CSV.value, file.CRAB_NEBULA_PDF.value])

create_task('Materia oscura', 'Mapear distribución', '2027-07-01', '2028-01-31', file.HEIC_1311_A_JPG.value, file.DEEP_SPACE_CSV.value)

create_task('Energía oscura', 'Estudiar expansión acelerada', '2027-08-10', '2028-02-10', [file.HEIC_1311_A_JPG.value, file.SOMBRERO_GALAXY_JPG.value], file.NGC_1514_PDF.value)

create_task('Astrofísica teórica', 'Desarrollar nuevos modelos', '2027-09-01', '2028-03-31', file.SOMBRERO_GALAXY_JPG.value, [file.CRAB_NEBULA_PDF.value, file.STARS_CSV.value])

create_task('Instrumentación', 'Probar nuevos detectores', '2027-10-15', '2028-04-15', file.HEIC_1311_A_JPG.value, file.DEEP_SPACE_CSV.value)

create_task('Historia astronómica', 'Documentar descubrimientos', '2027-11-01', '2028-05-31', file.SOMBRERO_GALAXY_JPG.value, file.NGC_1514_PDF.value)

create_task('Clima espacial', 'Predecir tormentas solares', '2028-01-10', '2028-07-10', [file.HEIC_1311_A_JPG.value, file.SOMBRERO_GALAXY_JPG.value], [file.STARS_CSV.value, file.DEEP_SPACE_CSV.value])

create_task('Galaxias activas', 'Estudiar núcleos galácticos', '2028-02-15', '2028-08-15', file.SOMBRERO_GALAXY_JPG.value, file.CRAB_NEBULA_PDF.value)

create_task('Estructura a gran escala', 'Mapear filamentos cósmicos', '2028-03-01', '2028-09-30', file.HEIC_1311_A_JPG.value, file.NGC_1514_PDF.value)

create_task('Telescopios virtuales', 'Probar interferometría', '2028-04-10', '2028-10-10', [file.HEIC_1311_A_JPG.value, file.SOMBRERO_GALAXY_JPG.value], file.DEEP_SPACE_CSV.value)

create_task('Vida en el universo', 'Evaluar ecuación de Drake', '2028-05-01', '2028-11-30', file.SOMBRERO_GALAXY_JPG.value, [file.STARS_CSV.value, file.NGC_1514_PDF.value])

create_task('Astronáutica', 'Planificar misiones futuras', '2028-06-15', '2028-12-15', file.HEIC_1311_A_JPG.value, file.CRAB_NEBULA_PDF.value)

create_task('Educación astronómica', 'Desarrollar material educativo', '2028-07-01', '2029-01-31', [file.HEIC_1311_A_JPG.value, file.SOMBRERO_GALAXY_JPG.value], file.DEEP_SPACE_CSV.value)

create_task('Software astronómico', 'Desarrollar herramientas', '2028-08-10', '2029-02-10', file.SOMBRERO_GALAXY_JPG.value, [file.CRAB_NEBULA_PDF.value, file.STARS_CSV.value])

create_task('Fotografía astronómica', 'Mejorar técnicas', '2028-09-01', '2029-03-31', file.HEIC_1311_A_JPG.value, file.NGC_1514_PDF.value)

create_task('Colisiones galácticas', 'Simular encuentros', '2028-10-15', '2029-04-15', file.SOMBRERO_GALAXY_JPG.value, file.DEEP_SPACE_CSV.value)

create_task('Exogeología', 'Estudiar geología planetaria', '2029-01-01', '2029-07-01', [file.HEIC_1311_A_JPG.value, file.SOMBRERO_GALAXY_JPG.value], [file.STARS_CSV.value, file.NGC_1514_PDF.value])

create_task('Atmósferas exoplanetarias', 'Analizar composición', '2029-02-01', '2029-08-31', file.SOMBRERO_GALAXY_JPG.value, file.CRAB_NEBULA_PDF.value)

create_task('Cinturón de Kuiper', 'Catalogar objetos', '2029-03-15', '2029-09-15', file.HEIC_1311_A_JPG.value, file.DEEP_SPACE_CSV.value)

create_task('Nube de Oort', 'Estudiar estructura', '2029-04-01', '2029-10-31', [file.HEIC_1311_A_JPG.value, file.SOMBRERO_GALAXY_JPG.value], file.STARS_CSV.value)

create_task('Galaxias enanas', 'Analizar propiedades', '2029-05-10', '2029-11-10', file.SOMBRERO_GALAXY_JPG.value, [file.CRAB_NEBULA_PDF.value, file.DEEP_SPACE_CSV.value])

create_task('Relatividad general', 'Probar predicciones', '2029-06-01', '2029-12-31', file.HEIC_1311_A_JPG.value, file.NGC_1514_PDF.value)

create_task('Meteoros', 'Estudiar lluvias de estrellas', '2029-07-15', '2030-01-15', [file.HEIC_1311_A_JPG.value, file.SOMBRERO_GALAXY_JPG.value], file.DEEP_SPACE_CSV.value)

create_task('Cosmología observacional', 'Recopilar datos', '2029-08-01', '2030-02-28', file.SOMBRERO_GALAXY_JPG.value, [file.STARS_CSV.value, file.NGC_1514_PDF.value])

create_task('Astronomía multimensajero', 'Combinar observaciones', '2029-09-10', '2030-03-10', file.HEIC_1311_A_JPG.value, file.CRAB_NEBULA_PDF.value)

create_task('Futuro de la astronomía', 'Planificar próximos telescopios', '2029-10-01', '2030-04-30', file.SOMBRERO_GALAXY_JPG.value, [file.DEEP_SPACE_CSV.value, file.CRAB_NEBULA_PDF.value, file.NGC_1514_PDF.value])